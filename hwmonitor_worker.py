import os
import time
import subprocess
import re
import psutil
import platform
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://influxdb:8086") # Use container name
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "cisco-super-secret-auth-token")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "cisco")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "metrics")
INTERVAL = int(os.getenv("MONITOR_INTERVAL", "2"))

def get_macos_gpu_info():
    gpu_cores = "N/A"
    if platform.system() != "Darwin":
        return gpu_cores
    try:
        sp = subprocess.check_output(['system_profiler', 'SPDisplaysDataType'], stderr=subprocess.DEVNULL, timeout=5).decode()
        for line in sp.split('\n'):
            if 'Total Number of Cores' in line:
                gpu_cores = line.strip().split(':')[-1].strip()
                break
    except Exception:
        pass
    return gpu_cores

def get_chip_label():
    try:
        res = subprocess.check_output(['system_profiler', 'SPHardwareDataType'], stderr=subprocess.DEVNULL, timeout=5).decode()
        for line in res.split('\n'):
            if 'Chip:' in line or 'chip:' in line:
                return line.strip().split(':', 1)[-1].strip()
        for line in res.split('\n'):
            if 'Apple M' in line:
                m = re.search(r'Apple M\d+\s*\w*', line)
                if m:
                    return m.group(0).strip()
    except Exception:
        pass
    return "Apple M-Series"

ST_CPU_COUNT = psutil.cpu_count()
ST_E_CORES = 4 if ST_CPU_COUNT >= 8 else 0
ST_P_CORES = ST_CPU_COUNT - ST_E_CORES
ST_RAM_TOTAL = round(psutil.virtual_memory().total / (1024**3), 2)
ST_GPU_CORES = get_macos_gpu_info()
ST_CHIP_LABEL = get_chip_label()

psutil.cpu_percent(percpu=True)

def get_macos_hw_stats():
    stats = {
        "e_cpu_pct": 0.0, "p_cpu_pct": 0.0,
        "gpu_pct": 0, "gpu_cores": ST_GPU_CORES,
        "ram_pct": 0.0, "ram_used_gb": 0.0, "ram_total_gb": ST_RAM_TOTAL,
        "e_cores": ST_E_CORES, "p_cores": ST_P_CORES,
        "cpu_power_w": -1, "gpu_power_w": -1, "total_power_w": -1,
        "chip_label": ST_CHIP_LABEL
    }
    try:
        percpu = psutil.cpu_percent(percpu=True)
        stats["e_cpu_pct"] = sum(percpu[:ST_E_CORES]) / ST_E_CORES if ST_E_CORES > 0 else sum(percpu) / len(percpu)
        stats["p_cpu_pct"] = sum(percpu[ST_E_CORES:]) / ST_P_CORES if ST_P_CORES > 0 else stats["e_cpu_pct"]

        mem = psutil.virtual_memory()
        stats["ram_pct"] = mem.percent
        stats["ram_used_gb"] = mem.used / (1024**3)
    except Exception:
        pass

    try:
        import plistlib
        pm_res = subprocess.check_output(['sudo', '-n', 'powermetrics', '-n', '1', '-i', '50', '--samplers', 'cpu_power,gpu_power', '-f', 'plist'], stderr=subprocess.DEVNULL, timeout=2)
        plist_data = plistlib.loads(pm_res)
        proc_data = plist_data.get('processor', {})
        if 'cpu_energy' in proc_data: stats["cpu_power_w"] = round(proc_data['cpu_energy'] / 1000.0, 2)
        if 'gpu_energy' in proc_data: stats["gpu_power_w"] = round(proc_data['gpu_energy'] / 1000.0, 2)
        if 'combined_power' in proc_data: stats["total_power_w"] = round(proc_data['combined_power'] / 1000.0, 2)
        elif 'processor_energy' in proc_data: stats["total_power_w"] = round(proc_data['processor_energy'] / 1000.0, 2)
        elif stats["cpu_power_w"] != -1 and stats["gpu_power_w"] != -1:
            ane_power_w = proc_data.get('ane_energy', 0) / 1000.0
            stats["total_power_w"] = round(stats["cpu_power_w"] + stats["gpu_power_w"] + ane_power_w, 2)
    except Exception:
        pass

    try:
        ioreg_res = subprocess.check_output(['ioreg', '-r', '-d', '1', '-c', 'IOAccelerator'], stderr=subprocess.DEVNULL, timeout=2).decode()
        m = re.search(r'"Device Utilization %"=(\d+)', ioreg_res)
        if m: stats["gpu_pct"] = int(m.group(1))
        m_gpow = re.search(r'"GPU Power"[\s:=]+(\d+\.?\d*)', ioreg_res)
        if m_gpow: stats["gpu_power_w"] = float(m_gpow.group(1)) / 1000.0
    except Exception:
        pass
    try:
        bat_res = subprocess.check_output(['ioreg', '-r', '-d', '1', '-c', 'AppleSmartBattery'], stderr=subprocess.DEVNULL, timeout=2).decode()
        current_m  = re.search(r'"InstantAmperage"=(\d+)', bat_res)
        voltage_m  = re.search(r'"Voltage"=(\d+)', bat_res)
        if current_m and voltage_m:
            amps = int(current_m.group(1))
            if amps > 0x7FFFFFFF: amps = -(0x100000000 - amps)
            if amps < 0:
                volts = int(voltage_m.group(1)) / 1000.0
                total_w = abs(amps) * volts / 1000.0
                stats["total_power_w"] = round(total_w, 2)
    except Exception:
        pass
    return stats


def main():
    print(f"Starting hardware monitor worker... Connecting to {INFLUXDB_URL}")
    while True:
        try:
            client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
            write_api = client.write_api(write_options=SYNCHRONOUS)
            
            # test connection
            if client.ping():
                print("Successfully connected to InfluxDB")
                break
        except Exception as e:
            print(f"Waiting for InfluxDB... {e}")
            time.sleep(5)
            
    while True:
        try:
            stats = get_macos_hw_stats()
            
            p = Point("hardware_monitor") \
                .tag("host", "mac_server") \
                .tag("chip", stats["chip_label"]) \
                .field("e_cpu_pct", float(stats.get("e_cpu_pct", 0))) \
                .field("p_cpu_pct", float(stats.get("p_cpu_pct", 0))) \
                .field("gpu_pct", float(stats.get("gpu_pct", 0))) \
                .field("ram_pct", float(stats.get("ram_pct", 0))) \
                .field("ram_used_gb", float(stats.get("ram_used_gb", 0))) \
                .field("cpu_power_w", float(stats.get("cpu_power_w", 0))) \
                .field("gpu_power_w", float(stats.get("gpu_power_w", 0))) \
                .field("total_power_w", float(stats.get("total_power_w", 0)))
                
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=p)
            print(f"Wrote data points to InfluxDB: CPU {stats['e_cpu_pct']:.1f}% / {stats['p_cpu_pct']:.1f}%")
        except Exception as e:
            print(f"Error writing to InfluxDB: {e}")
            
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()

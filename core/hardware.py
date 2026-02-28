import psutil
import subprocess
import re
import platform
import plistlib
from core.logger import logger

class HardwareMonitor:
    def __init__(self):
        self.cpu_count = psutil.cpu_count()
        # Heuristic for Apple Silicon core distribution
        self.e_cores = 4 if self.cpu_count >= 8 else 0
        self.p_cores = self.cpu_count - self.e_cores
        self.ram_total = round(psutil.virtual_memory().total / (1024**3), 2)
        self.gpu_cores = self._get_macos_gpu_info()
        self.chip_label = self._get_chip_label()
        
        # Initialize psutil counters
        psutil.cpu_percent(percpu=True)
        logger.info(f"Monitor Initialized: {self.chip_label} ({self.e_cores}E+{self.p_cores}P cores)")

    @staticmethod
    def _get_macos_gpu_info() -> str:
        """Get GPU core count (used at startup only)."""
        if platform.system() != "Darwin":
            return "N/A"
        try:
            sp = subprocess.check_output(['system_profiler', 'SPDisplaysDataType'],
                                         stderr=subprocess.DEVNULL, timeout=5).decode()
            for line in sp.split('\n'):
                if 'Total Number of Cores' in line:
                    return line.strip().split(':')[-1].strip()
        except Exception as e:
            logger.debug(f"GPU Info Error: {e}")
        return "N/A"

    @staticmethod
    def _get_chip_label() -> str:
        """Get Apple chip label (M1/M2/M3...) from system_profiler."""
        try:
            res = subprocess.check_output(['system_profiler', 'SPHardwareDataType'],
                                          stderr=subprocess.DEVNULL, timeout=5).decode()
            for line in res.split('\n'):
                if 'Chip:' in line or 'chip:' in line:
                    return line.strip().split(':', 1)[-1].strip()
            for line in res.split('\n'):
                if 'Apple M' in line:
                    m = re.search(r'Apple M\d+\s*\w*', line)
                    if m:
                        return m.group(0).strip()
        except Exception as e:
            logger.debug(f"Chip Label Error: {e}")
        return "Apple M-Series"

    def _get_basic_stats(self, stats: dict):
        """Collect CPU and RAM metrics."""
        percpu = psutil.cpu_percent(percpu=True)
        if self.e_cores > 0:
            stats["e_cpu_pct"] = sum(percpu[:self.e_cores]) / self.e_cores
            stats["p_cpu_pct"] = sum(percpu[self.e_cores:]) / self.p_cores
        else:
            stats["e_cpu_pct"] = sum(percpu) / len(percpu)
            stats["p_cpu_pct"] = stats["e_cpu_pct"]

        mem = psutil.virtual_memory()
        stats["ram_pct"] = mem.percent
        stats["ram_used_gb"] = mem.used / (1024**3)

    def _get_powermetrics_stats(self, stats: dict):
        """Collect power metrics via powermetrics command."""
        try:
            pm_res = subprocess.check_output(
                ['sudo', '-n', 'powermetrics', '-n', '1', '-i', '50', '--samplers', 'cpu_power,gpu_power', '-f', 'plist'],
                stderr=subprocess.DEVNULL, timeout=2
            )
            plist_data = plistlib.loads(pm_res)
            proc_data = plist_data.get('processor', {})
            
            if 'cpu_energy' in proc_data:
                stats["cpu_power_w"] = round(proc_data['cpu_energy'] / 1000.0, 2)
            if 'gpu_energy' in proc_data:
                stats["gpu_power_w"] = round(proc_data['gpu_energy'] / 1000.0, 2)
            
            # Total power fallback logic
            if 'combined_power' in proc_data:
                stats["total_power_w"] = round(proc_data['combined_power'] / 1000.0, 2)
            elif 'processor_energy' in proc_data:
                stats["total_power_w"] = round(proc_data['processor_energy'] / 1000.0, 2)
            elif stats["cpu_power_w"] != -1 and stats["gpu_power_w"] != -1:
                ane_power_w = proc_data.get('ane_energy', 0) / 1000.0
                stats["total_power_w"] = round(stats["cpu_power_w"] + stats["gpu_power_w"] + ane_power_w, 2)
        except Exception:
            pass # Silently fail if sudo nopasswd is not configured

    def _get_ioreg_stats(self, stats: dict):
        """Collect GPU utilization and power via ioreg."""
        try:
            ioreg_res = subprocess.check_output(['ioreg', '-r', '-d', '1', '-c', 'IOAccelerator'],
                                                stderr=subprocess.DEVNULL, timeout=2).decode()
            m_util = re.search(r'"Device Utilization %"=(\d+)', ioreg_res)
            if m_util:
                stats["gpu_pct"] = int(m_util.group(1))
            
            # Fallback GPU power if powermetrics failed
            if stats["gpu_power_w"] == -1.0:
                m_gpow = re.search(r'"GPU Power"[\s:=]+(\d+\.?\d*)', ioreg_res)
                if m_gpow:
                    stats["gpu_power_w"] = float(m_gpow.group(1)) / 1000.0
        except Exception:
            pass

    def _get_battery_power(self, stats: dict):
        """Estimate total power via battery discharge rate if not on AC."""
        if stats["total_power_w"] != -1.0:
            return
            
        try:
            bat_res = subprocess.check_output(
                ['ioreg', '-r', '-d', '1', '-c', 'AppleSmartBattery'],
                stderr=subprocess.DEVNULL, timeout=2).decode()
            current_m  = re.search(r'"InstantAmperage"=(\d+)', bat_res)
            voltage_m  = re.search(r'"Voltage"=(\d+)', bat_res)
            if current_m and voltage_m:
                amps = int(current_m.group(1))
                if amps > 0x7FFFFFFF:
                    amps = -(0x100000000 - amps)
                if amps < 0:
                    volts = int(voltage_m.group(1)) / 1000.0  
                    total_w = abs(amps) * volts / 1000.0  
                    stats["total_power_w"] = round(total_w, 2)
        except Exception:
            pass

    def get_stats(self) -> dict:
        """Collect all hardware metrics."""
        stats = {
            "e_cpu_pct": 0.0, "p_cpu_pct": 0.0,
            "gpu_pct": 0, "gpu_cores": self.gpu_cores,
            "ram_pct": 0.0, "ram_used_gb": 0.0, "ram_total_gb": self.ram_total,
            "e_cores": self.e_cores, "p_cores": self.p_cores,
            "cpu_power_w": -1.0, "gpu_power_w": -1.0, "total_power_w": -1.0,
            "chip_label": self.chip_label
        }
        
        self._get_basic_stats(stats)
        self._get_powermetrics_stats(stats)
        self._get_ioreg_stats(stats)
        self._get_battery_power(stats)

        return stats

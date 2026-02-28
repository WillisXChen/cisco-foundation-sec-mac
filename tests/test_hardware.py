import unittest
from unittest.mock import patch, MagicMock
from core.hardware import HardwareMonitor

class TestHardwareMonitor(unittest.TestCase):
    @patch('psutil.cpu_count')
    @patch('psutil.virtual_memory')
    @patch('subprocess.check_output')
    def test_init_and_get_stats(self, mock_subprocess, mock_vmem, mock_cpu_count):
        # Setup mocks
        mock_cpu_count.return_value = 10
        
        mock_mem_instance = MagicMock()
        mock_mem_instance.total = 16 * (1024**3)
        mock_mem_instance.percent = 50.0
        mock_mem_instance.used = 8 * (1024**3)
        mock_vmem.return_value = mock_mem_instance
        
        # Test initialization
        monitor = HardwareMonitor()
        self.assertEqual(monitor.cpu_count, 10)
        self.assertEqual(monitor.e_cores, 4)
        self.assertEqual(monitor.p_cores, 6)
        self.assertEqual(monitor.ram_total, 16.0)

        # Test get_stats
        with patch('psutil.cpu_percent') as mock_cpu_percent:
            mock_cpu_percent.return_value = [10.0] * 10  # 10 cores
            
            stats = monitor.get_stats()
            
            self.assertEqual(stats['e_cores'], 4)
            self.assertEqual(stats['p_cores'], 6)
            self.assertEqual(stats['e_cpu_pct'], 10.0)
            self.assertEqual(stats['p_cpu_pct'], 10.0)
            self.assertEqual(stats['ram_pct'], 50.0)
            self.assertEqual(stats['ram_used_gb'], 8.0)
            self.assertEqual(stats['ram_total_gb'], 16.0)

    @patch('platform.system')
    def test_get_macos_gpu_info_non_mac(self, mock_system):
        mock_system.return_value = "Windows"
        gpu_cores = HardwareMonitor._get_macos_gpu_info()
        self.assertEqual(gpu_cores, "N/A")

if __name__ == '__main__':
    unittest.main()

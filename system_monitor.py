"""
System Monitoring
Monitors system resources: CPU, Memory, Disk, Network, and Running Processes
"""

import psutil
import os
import json
import socket
import platform
from datetime import datetime
from pathlib import Path


class SystemMonitor:
    def __init__(self, log_file="system_monitor.log"):
        self.log_file = log_file
        self.ensure_log_file()
    
    def ensure_log_file(self):
        """Create log file if it doesn't exist"""
        Path(self.log_file).touch(exist_ok=True)
    
    def get_cpu_info(self):
        """Get CPU usage and core information"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_cores": psutil.cpu_count(logical=False),
            "cpu_threads": psutil.cpu_count(logical=True),
            "per_core_usage": psutil.cpu_percent(percpu=True, interval=1)
        }
    
    def get_memory_info(self):
        """Get memory usage information"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        return {
            "total_memory_gb": round(memory.total / (1024**3), 2),
            "used_memory_gb": round(memory.used / (1024**3), 2),
            "available_memory_gb": round(memory.available / (1024**3), 2),
            "memory_percent": memory.percent,
            "swap_total_gb": round(swap.total / (1024**3), 2),
            "swap_used_gb": round(swap.used / (1024**3), 2)
        }
    
    def get_disk_info(self):
        """Get disk usage for all partitions"""
        disk_info = {}
        for partition in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info[partition.device] = {
                    "mountpoint": partition.mountpoint,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent_used": usage.percent
                }
            except PermissionError:
                continue
        return disk_info
    
    def get_network_info(self):
        """Get network usage statistics"""
        net_io = psutil.net_io_counters()
        return {
            "bytes_sent": net_io.bytes_sent,
            "bytes_received": net_io.bytes_recv,
            "packets_sent": net_io.packets_sent,
            "packets_received": net_io.packets_recv
        }
    
    def get_top_processes(self, top_n=5):
        """Get top N processes by CPU and Memory usage"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        top_cpu = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)[:top_n]
        # Sort by memory usage
        top_memory = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:top_n]
        
        return {
            "top_cpu_processes": top_cpu,
            "top_memory_processes": top_memory
        }
    
    def get_system_info(self):
        """Get general system information"""
        return {
            "hostname": socket.gethostname(),
            "platform": platform.system(),
            "boot_time": datetime.fromtimestamp(psutil.boot_time()).isoformat(),
            "uptime_seconds": int(datetime.now().timestamp() - psutil.boot_time())
        }
    
    def monitor(self):
        """Collect all monitoring data"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "system": self.get_system_info(),
            "cpu": self.get_cpu_info(),
            "memory": self.get_memory_info(),
            "disk": self.get_disk_info(),
            "network": self.get_network_info(),
            "processes": self.get_top_processes()
        }
        return data
    
    def log_monitoring_data(self, data):
        """Log monitoring data to file"""
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(data, indent=2) + "\n" + "="*80 + "\n")
    
    def print_summary(self, data):
        """Print a formatted summary of system status"""
        print("\n" + "="*80)
        print(f"SYSTEM MONITORING REPORT - {data['timestamp']}")
        print("="*80)
        
        cpu = data['cpu']
        print(f"\n[CPU USAGE]")
        print(f"  Overall: {cpu['cpu_percent']}%")
        print(f"  Cores: {cpu['cpu_cores']} physical, {cpu['cpu_threads']} logical")
        
        mem = data['memory']
        print(f"\n[MEMORY USAGE]")
        print(f"  Used: {mem['used_memory_gb']} GB / {mem['total_memory_gb']} GB ({mem['memory_percent']}%)")
        print(f"  Available: {mem['available_memory_gb']} GB")
        
        print(f"\n[DISK USAGE]")
        for device, info in data['disk'].items():
            print(f"  {device} ({info['mountpoint']})")
            print(f"    Used: {info['used_gb']} GB / {info['total_gb']} GB ({info['percent_used']}%)")
        
        print(f"\n[TOP PROCESSES BY CPU]")
        for proc in data['processes']['top_cpu_processes'][:3]:
            print(f"  {proc['name']} (PID: {proc['pid']}) - {proc['cpu_percent']}%")
        
        print(f"\n[TOP PROCESSES BY MEMORY]")
        for proc in data['processes']['top_memory_processes'][:3]:
            print(f"  {proc['name']} (PID: {proc['pid']}) - {proc['memory_percent']}%")
        
        print("="*80 + "\n")


def main():
    """Main monitoring loop"""
    monitor = SystemMonitor()
    
    print("System Monitoring Started")
    print("Press Ctrl+C to stop monitoring\n")
    
    try:
        while True:
            # Collect monitoring data
            data = monitor.monitor()
            
            # Log to file
            monitor.log_monitoring_data(data)
            
            # Print summary
            monitor.print_summary(data)
            
            # Wait before next check (interval in seconds)
            import time
            time.sleep(5)
    
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")


if __name__ == "__main__":
    main()
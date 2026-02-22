# System Monitoring

A full-featured system monitoring application that tracks system resources and performance metrics.

## Features

- **CPU Monitoring**: Overall usage, per-core breakdown, core count
- **Memory Monitoring**: RAM usage, available memory, swap usage
- **Disk Monitoring**: Usage across all partitions and drives
- **Network Monitoring**: Bytes sent/received, packet counts
- **Process Monitoring**: Top processes by CPU and memory usage
- **System Info**: Hostname, boot time, uptime
- **Logging**: All data saved to JSON log file for analysis

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python system_monitor.py
```

The tool will:
1. Collect system metrics every 5 seconds
2. Display a formatted summary in the console
3. Log all data to `system_monitor.log` in JSON format

Press `Ctrl+C` to stop monitoring.

## Output

Console output shows:
- CPU usage percentage and core information
- Memory usage in GB and percentage
- Disk usage for all partitions
- Top 3 processes by CPU usage
- Top 3 processes by memory usage

Log file (`system_monitor.log`) contains complete JSON data for further analysis.

## Legitimate Use Cases

- System performance analysis
- Resource capacity planning
- Identifying resource-heavy processes
- IT infrastructure monitoring
- Educational purposes for system administration
- Performance troubleshooting

## Notes

- Some process information may require admin/elevated privileges
- Network stats show cumulative totals since system boot
- CPU percentages are sampled at 1-second intervals

# 🛡️ VPS Sentinel

A lightweight, zero-dependency Python script designed for Linux VPS auditing, resource monitoring, and security checks.

**Author:** Aaron  
**License:** GNU GPLv3

## 🚀 Features

* **Zero Dependencies:** Runs on standard Python 3 libraries. No `pip install` required.
* **System Audit:** Checks OS version, Kernel, Hostname, and Time.
* **Resource Monitoring:**
    * CPU Load (1m, 5m, 15m)
    * RAM Usage (calculates real usage without `psutil`)
    * Disk Usage
* **Security Checks:**
    * Detects if Root Login is enabled in SSH.
    * Checks Firewall status (UFW/IPTables).
* **Reporting:** Generates a JSON report (`vps_report.json`) for logs.

## 📥 Installation & Usage

Since it has no dependencies, you can simply download and run it.

```bash
# 1. Download the script
wget [https://raw.githubusercontent.com/aaron-devop/vps-sentinel-v1.0/main/vps_sentinel.py](https://raw.githubusercontent.com/aaron-devop/vps-sentinel-v1.0/main/vps_sentinel.py)

# 2. Run it (requires root for security checks)
sudo python3 vps_sentinel.py

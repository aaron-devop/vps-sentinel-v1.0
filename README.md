# 🛡️ VPS SENTINEL

![License](https://img.shields.io/github/license/aaron-devop/vps-sentinel-v1.0)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Size](https://img.shields.io/github/repo-size/aaron-devop/vps-sentinel-v1.0)

**A lightweight, zero-dependency Python script designed for Linux VPS auditing, resource monitoring, and security checks.**

This tool is designed for SysAdmins, DevOps engineers, and server owners who need a quick, professional snapshot of a server's health without installing heavy monitoring agents.

## 🚀 FEATURES

* **ZERO DEPENDENCIES:** Runs on standard Python 3 libraries. No `pip install` required.
* **SYSTEM AUDIT:** Checks OS version, Kernel, Hostname, Architecture, and Time.
* **RESOURCE MONITORING:**
    * **CPU:** Real-time Load Average (1m, 5m, 15m) & Core count.
    * **RAM:** Calculates real memory usage (reading `/proc/meminfo` directly).
    * **Disk:** Root partition usage analysis.
* **SECURITY CHECKS:**
    * **SSH Audit:** Detects if Root Login is enabled in `sshd_config`.
    * **Firewall:** Checks status of UFW or IPTables.
* **REPORTING:** Generates a structured JSON report (`vps_report.json`) for logs or external processing.

## 📥 INSTALLATION & USAGE

Since the script relies only on the Python Standard Library, you can run it immediately on any Linux server (Ubuntu, Debian, CentOS, etc.).

### ONE-LINE EXECUTION
You can download and run the script directly from the repository:

```bash
# 1. Download the script
wget [https://raw.githubusercontent.com/aaron-devop/vps-sentinel-v1.0/main/vps_sentinel.py](https://raw.githubusercontent.com/aaron-devop/vps-sentinel-v1.0/main/vps_sentinel.py)

# 2. Run it (sudo is required for reading system logs/configs)
sudo python3 vps_sentinel.py
```

## 📊 SAMPLE OUTPUT

When you run the script, you will see a colored terminal output like this:

```text
========================================
   VPS SENTINEL v1.0.0
========================================

--- [ Rendszer Információ ] ---
OS: Linux 5.4.0-100-generic | Kernel: x86_64
Host: production-server-01

--- [ Erőforrások ] ---
[✓] CPU Load (5m)            : 0.45 (Cores: 4)
[✓] RAM Használat            : 32.5% (Szabad: 4096 MB)
[✓] Lemez Használat (/)      : 45.0% (Szabad: 25 GB)

--- [ Biztonság ] ---
[!] SSH Root Login           : Root login enabled!
[✓] Tűzfal                   : UFW is active

Riport elmentve ide: vps_report.json
```

## 🛠️ REQUIREMENTS

* **OS:** Linux (Tested on Ubuntu 20.04/22.04, Debian 10/11, CentOS 7/8)
* **Python:** Python 3.6+
* **Permissions:** Root privileges (via `sudo`) are recommended for full security auditing (reading `/etc/ssh/sshd_config` and logs).

## 🤝 CONTRIBUTING

Contributions are always welcome!

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📜 LICENSE

Distributed under the GNU GPLv3 License. See `LICENSE` for more information.

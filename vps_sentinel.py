#!/usr/bin/env python3
"""
VPS Sentinel - Lightweight Server Audit Tool
Author: Aaron
Description: 
    Egyetlen fájlból álló, külső függőségek nélküli script 
    Linux VPS-ek gyors állapotfelmérésére és biztonsági auditálására.
Usage: 
    sudo python3 vps_sentinel.py
"""

import os
import sys
import subprocess
import json
import datetime
import shutil
import platform

# --- Configuration & Constants ---
VERSION = "1.0.0"
REPORT_FILE = "vps_report.json"

# ANSI Colors for nicer terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --- Helper Functions ---

def run_command(command):
    """Futtat egy shell parancsot és visszaadja a kimenetet."""
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

def print_status(label, status, value=""):
    """Szépített kimenet kiírása."""
    if status == "OK":
        symbol = f"{Colors.OKGREEN}[✓]{Colors.ENDC}"
    elif status == "WARN":
        symbol = f"{Colors.WARNING}[!]{Colors.ENDC}"
    elif status == "FAIL":
        symbol = f"{Colors.FAIL}[X]{Colors.ENDC}"
    else:
        symbol = f"{Colors.OKBLUE}[i]{Colors.ENDC}"
    
    print(f"{symbol} {Colors.BOLD}{label:<25}{Colors.ENDC} : {value}")

# --- Core Modules ---

class SystemAuditor:
    def get_system_info(self):
        uname = platform.uname()
        return {
            "os": f"{uname.system} {uname.release}",
            "hostname": uname.node,
            "architecture": uname.machine,
            "python_version": platform.python_version(),
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    def check_cpu_load(self):
        """Visszaadja a load average-et (1, 5, 15 perc)."""
        try:
            load1, load5, load15 = os.getloadavg()
            core_count = os.cpu_count()
            status = "OK"
            if load5 > core_count:
                status = "WARN" # Load magasabb mint a magok száma
            return {"status": status, "load_1m": load1, "load_5m": load5, "cores": core_count}
        except OSError:
            return {"status": "FAIL", "error": "Could not read load average"}

    def check_memory(self):
        """RAM használat olvasása /proc/meminfo-ból psutil nélkül."""
        try:
            mem_info = {}
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    parts = line.split(':')
                    if len(parts) == 2:
                        key = parts[0].strip()
                        val = int(parts[1].strip().split()[0]) # kB
                        mem_info[key] = val
            
            total = mem_info.get('MemTotal', 1)
            available = mem_info.get('MemAvailable', 0)
            used_percent = ((total - available) / total) * 100
            
            status = "OK"
            if used_percent > 85:
                status = "WARN"
            if used_percent > 95:
                status = "FAIL"
                
            return {
                "status": status,
                "total_mb": total // 1024,
                "available_mb": available // 1024,
                "used_percent": round(used_percent, 2)
            }
        except FileNotFoundError:
            return {"status": "FAIL", "error": "/proc/meminfo not found (Non-Linux?)"}

    def check_disk(self, path="/"):
        total, used, free = shutil.disk_usage(path)
        percent = (used / total) * 100
        status = "OK"
        if percent > 85: status = "WARN"
        if percent > 95: status = "FAIL"
        
        return {
            "status": status,
            "total_gb": total // (2**30),
            "free_gb": free // (2**30),
            "percent": round(percent, 2)
        }

class SecurityAuditor:
    def check_root_login(self):
        """Megnézi, hogy engedélyezve van-e a root login SSH-n."""
        sshd_config = "/etc/ssh/sshd_config"
        status = "UNKNOWN"
        details = "Config not found"
        
        if os.path.exists(sshd_config):
            try:
                with open(sshd_config, 'r') as f:
                    for line in f:
                        if line.strip().startswith("PermitRootLogin"):
                            if "yes" in line:
                                status = "FAIL"
                                details = "Root login enabled!"
                            elif "no" in line or "prohibit-password" in line:
                                status = "OK"
                                details = "Root login disabled/restricted"
                            break
            except PermissionError:
                status = "FAIL"
                details = "Permission denied (run as root)"
        
        return {"status": status, "details": details}

    def check_firewall(self):
        """UFW (Ubuntu/Debian) állapot ellenőrzése."""
        ufw_status = run_command("ufw status")
        if ufw_status:
            if "inactive" in ufw_status:
                return {"status": "WARN", "details": "UFW is inactive"}
            else:
                return {"status": "OK", "details": "UFW is active"}
        else:
             # Fallback: check iptables chains
            iptables = run_command("iptables -L")
            if iptables:
                 return {"status": "OK", "details": "IPTables rules found (manual check advised)"}
            return {"status": "UNKNOWN", "details": "No firewall detected"}

# --- Main Logic ---

def main():
    # Fejléc
    print(f"{Colors.HEADER}{'='*40}")
    print(f"   VPS SENTINEL v{VERSION}")
    print(f"{'='*40}{Colors.ENDC}")

    # Jogosultság ellenőrzés
    if os.geteuid() != 0:
        print(f"{Colors.WARNING}Figyelem: Nem root-ként futtatod. Néhány ellenőrzés sikertelen lehet.{Colors.ENDC}\n")

    sys_auditor = SystemAuditor()
    sec_auditor = SecurityAuditor()
    
    report = {}

    # 1. Rendszer Infó
    print(f"\n{Colors.BOLD}--- [ Rendszer Információ ] ---{Colors.ENDC}")
    sys_info = sys_auditor.get_system_info()
    report['system'] = sys_info
    print(f"OS: {sys_info['os']} | Kernel: {sys_info['architecture']}")
    print(f"Host: {sys_info['hostname']}")

    # 2. Erőforrások
    print(f"\n{Colors.BOLD}--- [ Erőforrások ] ---{Colors.ENDC}")
    
    # CPU
    cpu = sys_auditor.check_cpu_load()
    report['cpu'] = cpu
    print_status("CPU Load (5m)", cpu['status'], f"{cpu.get('load_5m', '?')} (Magok: {cpu.get('cores')})")
    
    # MEM
    mem = sys_auditor.check_memory()
    report['memory'] = mem
    print_status("RAM Használat", mem['status'], f"{mem.get('used_percent', '?')}% (Szabad: {mem.get('available_mb', '?')} MB)")

    # DISK
    disk = sys_auditor.check_disk()
    report['disk'] = disk
    print_status("Lemez Használat (/)", disk['status'], f"{disk.get('percent')}% (Szabad: {disk.get('free_gb')} GB)")

    # 3. Biztonság
    print(f"\n{Colors.BOLD}--- [ Biztonság ] ---{Colors.ENDC}")
    
    # SSH
    ssh = sec_auditor.check_root_login()
    report['ssh_root'] = ssh
    print_status("SSH Root Login", ssh['status'], ssh['details'])

    # Firewall
    fw = sec_auditor.check_firewall()
    report['firewall'] = fw
    print_status("Tűzfal", fw['status'], fw['details'])

    # 4. Report mentés
    try:
        with open(REPORT_FILE, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"\n{Colors.OKBLUE}Riport elmentve ide: {REPORT_FILE}{Colors.ENDC}")
    except IOError as e:
        print(f"\n{Colors.FAIL}Hiba a riport mentésekor: {e}{Colors.ENDC}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nKilépés...")
                  

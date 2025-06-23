# thunder_web_scanner.py
# Thunder Web Scanner: Automated Recon & Enumeration Tool

import os
import subprocess
import argparse
import datetime
from pathlib import Path

# ========== BANNER ==========
BANNER = r'''
  _____ _                     _            __        __   _     
 |_   _| |__  _   _ _ __   __| | ___ _ __  \ \      / /__| |__  
   | | | '_ \| | | | '_ \ / _` |/ _ \ '__|  \ \ /\ / / _ \ '_ \ 
   | | | | | | |_| | | | | (_| |  __/ |      \ V  V /  __/ |_) |
  _|_| |_| |_|\__,_|_| |_|\__,_|\___|_|       \_/\_/ \___|_.__/ 
 / ___|  ___ __ _ _ __  _ __   ___ _ __                         
 \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|                        
  ___) | (_| (_| | | | | | | |  __/ |                           
 |____/ \___\__,_|_| |_|_| |_|\___|_|                           
                                                                                 
                   ⚡ Thunder Web Scanner ⚡
        Automated Directory & Domain Recon Tool
'''

# ========== CONFIG ==========
OUTPUT_DIR = Path("output") / datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
TOOLS = {
    "dirb": "dirb",
    "gobuster": "gobuster",
    "ffuf": "ffuf",
    "dnsenum": "dnsenum",
    "amass": "amass",
    "subfinder": "subfinder",
    "wget": "wget"
}

# ========== FUNCTIONS ==========
def run_command(command, output_file):
    with open(output_file, 'w') as out:
        process = subprocess.Popen(command, shell=True, stdout=out, stderr=subprocess.STDOUT)
        process.communicate()


def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)


def run_dir_scanners(target):
    print("[+] Running Directory Scanners...")
    path = OUTPUT_DIR / "directories"
    ensure_dir(path)

    run_command(f"{TOOLS['dirb']} http://{target} -o {path}/dirb.txt", path / "dirb.txt")
    run_command(f"{TOOLS['gobuster']} dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt -o {path}/gobuster.txt", path / "gobuster.txt")
    run_command(f"{TOOLS['ffuf']} -u http://{target}/FUZZ -w /usr/share/wordlists/dirb/common.txt -o {path}/ffuf.json -of json", path / "ffuf.json")


def run_subdomain_scanners(domain):
    print("[+] Running Subdomain Scanners...")
    path = OUTPUT_DIR / "subdomains"
    ensure_dir(path)

    run_command(f"{TOOLS['dnsenum']} {domain} > {path}/dnsenum.txt", path / "dnsenum.txt")
    run_command(f"{TOOLS['amass']} enum -d {domain} -o {path}/amass.txt", path / "amass.txt")
    run_command(f"{TOOLS['subfinder']} -d {domain} -o {path}/subfinder.txt", path / "subfinder.txt")


def run_page_crawler(domain):
    print("[+] Crawling Pages...")
    path = OUTPUT_DIR / "crawler"
    ensure_dir(path)

    run_command(f"{TOOLS['wget']} --mirror --convert-links --adjust-extension --page-requisites --no-parent http://{domain} -P {path}", path / "wget.txt")


def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Thunder Web Scanner: Automated Recon & Enumeration Tool")
    parser.add_argument("target", help="Target IP or domain")
    args = parser.parse_args()

    ensure_dir(OUTPUT_DIR)

    run_dir_scanners(args.target)
    run_subdomain_scanners(args.target)
    run_page_crawler(args.target)

    print(f"\n[✓] Scan complete. Results saved in: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()

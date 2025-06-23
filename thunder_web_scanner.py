import subprocess
import argparse
import shutil

# ========== BANNER ==========
BANNER = '''
\033[96m
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
 Subdomains | Directories | Services | Technologies
\033[0m
'''

TOOLS = {
    "subfinder": "subfinder",
    "amass": "amass",
    "dnsenum": "dnsenum",
    "gobuster": "gobuster",
    "ffuf": "ffuf",
    "nmap": "nmap",
    "whatweb": "whatweb"
}

def check_tool(tool):
    return shutil.which(tool) is not None

def run_command(command, title):
    print(f"\n\033[92m[+] Running: {title}\033[0m\n{'='*60}")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"\033[91m[!] Failed: {title}\033[0m")

# ========== MODULES ==========
def scan_subdomains(domain):
    if check_tool("subfinder"):
        run_command(f"subfinder -d {domain}", "Subfinder")
    if check_tool("amass"):
        run_command(f"amass enum -d {domain}", "Amass Subdomain Enum")
    if check_tool("dnsenum"):
        run_command(f"dnsenum {domain}", "DNSenum")

def scan_directories(domain):
    if check_tool("gobuster"):
        run_command(f"gobuster dir -u http://{domain} -w /usr/share/wordlists/dirb/common.txt", "Gobuster Directory Scan")
    elif check_tool("ffuf"):
        run_command(f"ffuf -u http://{domain}/FUZZ -w /usr/share/wordlists/dirb/common.txt", "FFUF Directory Scan")

def scan_services(domain):
    if check_tool("nmap"):
        run_command(f"nmap -sV -Pn {domain}", "Nmap Service & Version Detection")

def scan_technologies(domain):
    if check_tool("whatweb"):
        run_command(f"whatweb http://{domain}", "WhatWeb Technology Fingerprint")

# ========== MAIN ==========
def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="Thunder Web Scanner: Subdomains, Directories, Services, Tech Detection")
    parser.add_argument("target", help="Target domain or IP (e.g., example.com)")
    args = parser.parse_args()

    scan_subdomains(args.target)
    scan_directories(args.target)
    scan_services(args.target)
    scan_technologies(args.target)

    print("\n\033[96m[✓] Scan completed successfully.\033[0m")

if __name__ == "__main__":
    main()

import os
import subprocess
import argparse
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ========== BANNER ==========
BANNER = Fore.CYAN + r'''
  _____ _                     _            __        __   _     
 |_   _| |__  _   _ _ __   __| | ___ _ __  \ \      / /__| |__  
   | | | '_ \| | | | '_ \ / _` |/ _ \ '__|  \ \ /\ / / _ \ '_ \ 
   | | | | | | |_| | | | | (_| |  __/ |      \ V  V /  __/ |_) |
  _|_| |_| |_|\__,_|_| |_|\__,_|\___|_|       \_/\_/ \___|_.__/ 
 / ___|  ___ __ _ _ __  _ __   ___ _ __                         
 \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|                        
  ___) | (_| (_| | | | | | | |  __/ |                           
 |____/ \___\__,_|_| |_|_| |_|\___|_|                           

''' + Style.RESET_ALL + Fore.YELLOW + r'''
                   ⚡ Thunder Web Scanner ⚡
        Automated Directory & Domain Recon Tool
''' + Style.RESET_ALL

# ========== TOOL CONFIG ==========
TOOLS = {
    "dirb": "dirb",
    "gobuster": "gobuster",
    "ffuf": "ffuf",
    "dnsenum": "dnsenum",
    "amass": "amass",
    "subfinder": "subfinder",
    "wget": "wget"
}

# ========== COMMAND EXECUTOR ==========
def run_command(command, title):
    print(Fore.GREEN + f"\n[+] Running: {title}\n" + Fore.WHITE + "="*60)
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(Fore.RED + f"[!] Error running: {title}")

# ========== MODULES ==========
def run_dir_scanners(target):
    run_command(f"{TOOLS['dirb']} http://{target}", "DIRB Scanner")
    run_command(f"{TOOLS['gobuster']} dir -u http://{target} -w /usr/share/wordlists/dirb/common.txt", "Gobuster Scanner")
    run_command(f"{TOOLS['ffuf']} -u http://{target}/FUZZ -w /usr/share/wordlists/dirb/common.txt", "FFUF Scanner")

def run_subdomain_scanners(domain):
    run_command(f"{TOOLS['dnsenum']} {domain}", "DNSenum")
    run_command(f"{TOOLS['amass']} enum -d {domain}", "Amass Subdomain Enum")
    run_command(f"{TOOLS['subfinder']} -d {domain}", "Subfinder")

def run_page_crawler(domain):
    run_command(f"{TOOLS['wget']} --spider --recursive --level=1 --no-parent http://{domain}", "Wget Spider (no download)")

# ========== MAIN ==========
def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description="Thunder Web Scanner: Automated Recon & Enumeration Tool")
    parser.add_argument("target", help="Target IP or domain")
    parser.add_argument("--dir", action="store_true", help="Run directory scanners")
    parser.add_argument("--sub", action="store_true", help="Run subdomain scanners")
    parser.add_argument("--crawl", action="store_true", help="Run page crawler")
    args = parser.parse_args()

    if not (args.dir or args.sub or args.crawl):
        print(Fore.RED + "[!] No scan type selected. Use --dir, --sub, and/or --crawl.")
        return

    if args.dir:
        run_dir_scanners(args.target)
    if args.sub:
        run_subdomain_scanners(args.target)
    if args.crawl:
        run_page_crawler(args.target)

    print(Fore.CYAN + "\n[✓] Scan complete." + Style.RESET_ALL)

if __name__ == "__main__":
    main()

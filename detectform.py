import requests
from bs4 import BeautifulSoup
from colorama import Fore, init
import urllib3

init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print(Fore.RED + "\n[ BruteSqli - Deteksi Form Login ]")
print(Fore.WHITE + "→ Mendeteksi input type 'text' dan 'password'\n")

# Input URL
url = input(Fore.YELLOW + "Masukkan URL form login (contoh: https://target.com/login.php):\n> ").strip()

try:
    res = requests.get(url, timeout=10, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Cari form
    form = soup.find('form')
    if not form:
        print(Fore.RED + "[!] Tidak ditemukan <form> pada halaman.")
        exit()

    # Deteksi input
    input_text = soup.find('input', {'type': 'text'})
    input_pass = soup.find('input', {'type': 'password'})

    user_field = input_text.get('name') if input_text else None
    pass_field = input_pass.get('name') if input_pass else None

    if user_field and pass_field:
        print(Fore.GREEN + "[✓] Ditemukan input login form:")
        print(Fore.YELLOW + f"    - Username field: {user_field}")
        print(Fore.YELLOW + f"    - Password field: {pass_field}")

        # Optional: Simpan ke file
        with open("form_fields.txt", "w") as f:
            f.write(f"{user_field},{pass_field}")
    else:
        print(Fore.RED + "[!] Form ditemukan, tapi tidak bisa mendeteksi input username atau password.")

except Exception as e:
    print(Fore.LIGHTRED_EX + f"[!] Error saat mengakses halaman: {e}")

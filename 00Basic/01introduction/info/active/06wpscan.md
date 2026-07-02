# WPScan
## Penjelasan WPScan

**WPScan** adalah scanner keamanan _black-box_ yang dirancang khusus untuk mengaudit situs WordPress. Tool ini bisa mendeteksi versi WordPress, plugin, tema, user, serta kerentanan yang diketahui (CVE) dengan bantuan database dari WPScan API.

WPScan bersifat **open-source** (Ruby-based) dan banyak digunakan dalam penetration testing di lingkungan WordPress.

### Teknik yang Digunakan WPScan

| Teknik | Penjelasan |
|---|---|
| **Fingerprinting Versi** | Membaca file `/readme.html`, `/license.txt`, `/wp-includes/version.php`, generator tag di HTML, serta hash CSS/JS untuk menentukan versi WP. |
| **Plugin & Theme Enumeration** | Brute-force nama plugin/theme dari _database wordlist_ (~20rb+ entri), lalu cek keberadaan file README, changelog, atau pattern spesifik. |
| **User Enumeration** | Memanfaatkan REST API `/wp-json/wp/v2/users/`, error message login (ketika username benar vs salah), dan author archive (`?author=N`). |
| **Vulnerability Lookup** | Mencocokkan versi WP, plugin, dan theme yang terdeteksi dengan database kerentanan (via API atau lokal). |
| **Password Brute-force** | Mendukung serangan brute-force pada halaman `wp-login.php`, XML-RPC, dan `wp-json`. |
| **Timthumb Detection** | Deteksi file `timthumb.php` yang mungkin rentan. |
| **Config Backup Finder** | Mencari backup file konfigurasi seperti `wp-config.php~`, `.wp-config.php.swp`, dll. |

### Cara Install WPScan

#### 1. Install di Kali Linux (sudah include)
```bash
sudo apt update && sudo apt install wpscan -y
```

#### 2. Install via Ruby (manual/cross-platform)
```bash
# Install Ruby dan dependencies
sudo apt install ruby ruby-dev libcurl4-openssl-dev zlib1g-dev build-essential -y

# Install WPScan via gem
sudo gem install wpscan
```

#### 3. Install via Docker
```bash
docker pull wpscanteam/wpscan
docker run --rm -it wpscanteam/wpscan --url <TARGET_URL>
```

### Cara Menggunakan WPScan

```bash
# Scan dasar - deteksi versi WP dan informasi umum
wpscan --url http://target.com

# Enumerasi user
wpscan --url http://target.com --enumerate u

# Enumerasi plugin yang vulnerable (butuh API token - gratis di wpscan.com/register)
wpscan --url http://target.com --enumerate vp --api-token YOUR_API_TOKEN

# Enumerasi semua kerentanan (plugin + theme + WP core)
wpscan --url http://target.com --enumerate v --api-token YOUR_API_TOKEN

# Brute-force login
wpscan --url http://target.com --passwords /path/to/wordlist.txt --usernames admin

# Scan lebih agresif (deteksi plugin via passive + aggressive)
wpscan --url http://target.com --enumerate ap --plugins-detection aggressive
```

### Alur Kerja WPScan

```
                   +---------------------------+
                   |   Target URL (--url)      |
                   +-------------+-------------+
                                 |
                    +------------v-------------+
                    | 1. HTTP Response Check   |
                    |  - Apakah server hidup?  |
                    |  - Apakah ini WordPress? |
                    +------------+-------------+
                                 |
                    +------------v-------------+
                    | 2. Passive Detection     |
                    |  - Generator tag, meta   |
                    |  - File readme, license  |
                    |  - Version fingerprint   |
                    +------------+-------------+
                                 |
                    +------------v-------------+
                    | 3. Enumeration           |
                    |  - Users (--enumerate u) |
                    |  - Plugins (vp, ap, p)   |
                    |  - Themes (vt, at, t)    |
                    |  - Timthumb, config bk   |
                    +------------+-------------+
                                 |
                    +------------v-------------+
                    | 4. Vulnerability Lookup  |
                    |  - Cocokkan dg database  |
                    |  - (API token diperlukan)|
                    +------------+-------------+
                                 |
                    +------------v-------------+
                    | 5. Output Report         |
                    |  - Versi WP & kerentanan |
                    |  - Plugin/theme rentan   |
                    |  - User terdaftar        |
                    +--------------------------+
```

### Script Python Sederhana (Mini WordPress User Scanner)

Script di bawah mensimulasikan teknik enumerasi user seperti WPScan dengan memanfaatkan REST API WordPress dan author archive.

```python
#!/usr/bin/env python3
"""
Mini WordPress User Enumerator - terinspirasi dari WPScan
Mendeteksi user via REST API dan author archive
"""

import requests
import sys
import re
from concurrent.futures import ThreadPoolExecutor

class WPScanner:
    def __init__(self, url, threads=5):
        self.base_url = url.rstrip('/')
        self.threads = threads
        self.users = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scan_rest_api(self):
        """Enum user via /wp-json/wp/v2/users/"""
        rest_url = f"{self.base_url}/wp-json/wp/v2/users"
        try:
            resp = self.session.get(rest_url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                for user in data:
                    self.users.append({
                        'id': user.get('id'),
                        'username': user.get('slug') or user.get('name'),
                        'name': user.get('name'),
                        'method': 'REST API'
                    })
                print(f"[+] REST API: Ditemukan {len(data)} user")
                return True
            elif resp.status_code == 403:
                print("[-] REST API diblokir (403)")
            else:
                print(f"[-] REST API: HTTP {resp.status_code}")
        except Exception as e:
            print(f"[!] REST API error: {e}")
        return False
    
    def scan_author_archive(self, start=1, end=20):
        """Enum user via ?author=N redirect"""
        print(f"[*] Mengecek author archive (ID {start}-{end})...")
        for uid in range(start, end + 1):
            url = f"{self.base_url}/?author={uid}"
            try:
                resp = self.session.get(url, timeout=10, allow_redirects=True)
                if resp.status_code == 200:
                    # Cek pola di URL setelah redirect (contoh: /author/username/)
                    author_match = re.search(r'/author/([^/]+)', resp.url)
                    if author_match:
                        username = author_match.group(1)
                        # Cegah duplikasi
                        if not any(u['username'] == username for u in self.users):
                            self.users.append({
                                'id': uid,
                                'username': username,
                                'name': username,
                                'method': f'Author Archive (ID {uid})'
                            })
                            print(f"  [+] ID {uid} -> {username}")
            except Exception:
                pass
    
    def scan_login_error(self, usernames):
        """Deteksi valid username via pesan error wp-login.php"""
        print("[*] Menguji username via login error message...")
        for username in usernames:
            data = {
                'log': username,
                'pwd': 'wrongpassword123456'
            }
            try:
                resp = self.session.post(
                    f"{self.base_url}/wp-login.php",
                    data=data,
                    timeout=10
                )
                text = resp.text
                # WP error: "Error: The password you entered for the username X is incorrect."
                # Berbeda dengan "Error: Invalid username."
                if 'incorrect' in text.lower() and username.lower() in text.lower():
                    if not any(u['username'] == username for u in self.users):
                        self.users.append({
                            'id': '?',
                            'username': username,
                            'name': username,
                            'method': 'Login Error'
                        })
                        print(f"  [+] Login Error -> {username} valid")
                # Cek juga untuk email
                elif 'unknown email address' in text.lower() or 'invalid email' in text.lower():
                    pass  # Email tidak valid
            except Exception:
                pass
    
    def run(self):
        print(f"{'='*50}")
        print(f"WPScanner Lite -> {self.base_url}")
        print(f"{'='*50}\n")
        
        # Tahap 1: REST API
        self.scan_rest_api()
        
        # Tahap 2: Author Archive
        self.scan_author_archive(1, 15)
        
        # Tahap 3: Login Error (jika ada username dari metode sebelumnya)
        if self.users:
            usernames = [u['username'] for u in self.users]
            self.scan_login_error(usernames)
        
        # Hasil
        print(f"\n{'='*50}")
        print(f"HASIL: {len(self.users)} user ditemukan")
        print(f"{'='*50}")
        for u in self.users:
            print(f"  - {u['username']:20s} | {u['method']}")
        
        return self.users

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 wp_scanner.py <URL>")
        print("Example: python3 wp_scanner.py http://example.com")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = WPScanner(target)
    scanner.run()
```

Cara pakai:
```bash
python3 wp_scanner.py http://target.com
```

---
### Pertanyaan
Perintah apa ini ?
- wpscan --url http://192.168.10.189 --enumerate u
- wpscan --url http://192.168.10.189 --enumerate vp --api-token [API]
- wpscan --url http://192.168.10.189 --enumerate vt --api-token [API]

### Jawaban Perintah yang Ditanyakan

```bash
1. wpscan --url http://192.168.10.189 --enumerate u
```
**Perintah ini** melakukan enumerasi user WordPress pada target `http://192.168.10.189`. WPScan akan mendeteksi username yang terdaftar melalui REST API, author archive (`?author=N`), dan pola login error. **Tidak perlu API token** untuk enumerasi user.

```bash
2. wpscan --url http://192.168.10.189 --enumerate vp
```
**Enumerasi plugin yang vulnerable (rentan)**. WPScan akan mendeteksi plugin yang terpasang dan mencocokkannya dengan database kerentanan. **Dengan API token**, hasilnya akan menunjukkan plugin mana yang punya CVE dan link referensinya. **Tanpa API token**, hanya akan menampilkan versi plugin saja tanpa informasi kerentanan.

```bash
3. wpscan --url http://192.168.10.189 --enumerate vp --api-token <API>
```
Sama seperti no.2, tapi **dengan API token** aktif. Token ini memungkinkan WPScan mengakses database WPScan API (cloud) untuk mencocokkan versi plugin dengan daftar kerentanan yang diketahui. Hasilnya berupa output detail seperti:
```
[+] plugin-name
   | Location: /wp-content/plugins/plugin-name/
   | Version: 1.2.3
   | Found By: Readme
   | [!] 1 vulnerability identified:
   | [!] Title: Plugin X 1.2.3 - SQL Injection
   |     CVE: CVE-2024-XXXXX
```

```bash
4. wpscan --url http://192.168.10.189 --enumerate vt --api-token <API>
```
**Enumerasi theme yang vulnerable**. Sama seperti `vp` (vulnerable plugins) tapi untuk theme. WPScan akan mendeteksi theme aktif maupun tidak aktif, lalu mencocokkan versinya dengan database kerentanan theme via API.

### Kenapa Harus Login untuk Mendapatkan API Token?

Mentor Anda benar. WPScan API adalah layanan **cloud-based** yang dikelola oleh WPSecure (pengembang WPScan). Alasan kenapa harus registrasi:

1. **Rate limiting** — API gratis dibatasi (25 permintaan/hari untuk akun free) untuk mencegah penyalahgunaan.
2. **Database up-to-date** — Database kerentanan diperbarui terus menerus dan disimpan di server mereka, bukan di tool lokal.
3. **Identifikasi pengguna** — Untuk audit dan akuntabilitas, wajar bagi layanan publik untuk meminta registrasi.
4. **Fitur premium** — Akun berbayar (API-WPScan) memberikan akses tak terbatas dan update real-time.

**Cara mendapatkannya:**
1. Buka [https://wpscan.com/register](https://wpscan.com/register)
2. Daftar (gratis)
3. Masuk ke dashboard → copy **API Token**
4. Gunakan: `wpscan --url <URL> --api-token <TOKEN_KAMU>`

Tanpa API token, WPScan tetap bisa jalan untuk enumerasi user/fingerprinting, tapi **tidak bisa menampilkan informasi kerentanan spesifik** (CVE, CVSS, link referensi). Ini yang membedakan output perintah no.2 vs no.3 di atas.

[Previously](05Nmap.md) | [Next](#)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
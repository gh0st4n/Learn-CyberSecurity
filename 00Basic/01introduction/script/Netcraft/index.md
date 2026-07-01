# Script Python
[netcraft_lite.py](netcraft_lite.py)

# Cara Install & Jalankan

### 1. Install dependencies:
```bash
pip install requests dnspython beautifulsoup4 pyOpenSSL
```

### 2. Jalankan:

bash

```
python3 netcraft_lite.py example.com
# atau
python3 netcraft_lite.py https://target.com
```
## Contoh Output

```
╔═══════════════════════════════════════════╗
║       NetCraft-Lite — Website Recon       ║
╚═══════════════════════════════════════════╝

Target: https://example.com
Started at: 2026-07-01 10:30:00
=======================================================

[+] DNS Enumeration untuk: example.com

  IPv4 Address:
    → 93.184.216.34

  Mail Servers:
    → example.com. 10 mail.example.com.

  Nameservers:
    → a.iana-servers.net.
    → b.iana-servers.net.

  TXT Records:
    → "v=spf1 -all"

[+] IP Address: 93.184.216.34

[+] HTTP Response Headers:
  Server: Apache/2.4.41
  Content-Type: text/html; charset=UTF-8

[+] Detected Technologies:
  ✓ Apache (confidence: 100%)
    └─ Header Server: Apache/2.4.41

[+] SSL/TLS Certificate Analysis:
  Common Name (CN): example.com
  Issuer: Let's Encrypt
  Valid Until: 2026-09-28
  ✓ Valid for 89 days

  Subject Alternative Names (SAN):
    → example.com
    → www.example.com
    → admin.example.com

=======================================================
Recon selesai. Target: example.com
=======================================================
```
## Fitur yang Bisa Dikembangkan Sendiri

|Fitur Tambahan|Deskripsi|Library|
|---|---|---|
|Subdomain brute force|Coba wordlist subdomain|`dns.resolver` + wordlist|
|Port scanning|Scan port umum (22,80,443,8080)|`socket`|
|Screenshot|Ambil screenshot website|`selenium` atau `playwright`|
|Wayback Machine|Cari history URL target|`requests` ke `web.archive.org`|
|WAF Detection|Deteksi Web Application Firewall|Header pattern matching|
|Directory fuzzing|Cari direktori tersembunyi|`requests` + wordlist|
|Javascript analysis|Ekstrak endpoint dari JS|`beautifulsoup4` + regex|
|Export CSV/JSON|Simpan hasil ke file|`json`, `csv`|

Script ini memberikan recon passif penuh tanpa menyentuh target secara agresif - sempurna untuk fase _reconnaissance_ dalam penetration testing.

[Previously](../../info/pasive/01GDorking.md) | [Next](../../info/active/00Whois.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
# crt.sh — Teknik, Penggunaan, Alur Kerja, Tips & Trick, Cheatsheet

**crt.sh** adalah Certificate Transparency (CT) log search engine yang dikelola oleh Sectigo (Comodo CA). Layanan ini memungkinkan siapa saja untuk mencari sertifikat SSL/TLS yang pernah diterbitkan oleh Certificate Authority (CA) yang berpartisipasi dalam program Certificate Transparency.

## 1. Apa Itu Certificate Transparency (CT)?

CT adalah sistem kerangka kerja publik yang mewajibkan semua CA untuk mencatat setiap sertifikat yang mereka terbitkan ke dalam log publik. Tujuan awalnya adalah untuk mendeteksi sertifikat palsu atau salah penerbitan, tetapi bagi seorang penetration tester, CT log adalah **goldmine reconnaissance pasif**.

Setiap entri di log CT berisi:
- **Common Name (CN)** — domain utama
- **Subject Alternative Name (SAN)** — seluruh domain yang tercakup
- **Issuer** — CA yang menerbitkan
- **Validity period** — tanggal berlaku
- **Serial number** & **Fingerprint SHA-256**

## 2. Teknik yang Digunakan oleh Netcraft

**Netcraft** menggunakan crt.sh sebagai salah satu sumber data intelijen untuk layanan **Site Report** dan **Security Testing** mereka. Secara spesifik:

### A. Subdomain Discovery
Netcraft mengambil semua sertifikat yang tercatat untuk suatu domain dari crt.sh, lalu mengekstrak **SAN** (Subject Alternative Name) untuk menemukan subdomain yang mungkin tidak terlihat dari sumber lain.

### B. Validasi Sertifikat & Usia
Netcraft membandingkan tanggal penerbitan dan kadaluarsa sertifikat untuk menentukan usia domain, pergantian sertifikat, dan potensi kelemahan (misal: sertifikat yang sudah expired tapi masih aktif).

### C. Fingerprinting Server
Dengan menggabungkan data CT + data scan langsung, Netcraft dapat mengidentifikasi teknologi server, versi SSL/TLS, dan konfigurasi keamanan.

### D. Exposure Assessment
Mendeteksi domain yang memiliki SAN terlalu luas (wildcard berlebihan) atau sertifikat dari CA yang kurang terpercaya.

### E. Phishing Detection
Netcraft menggunakan data historis CT untuk mendeteksi domain yang baru didaftarkan dan langsung mendapatkan sertifikat — indikasi potensi phishing.

## 3. Cara Menggunakan crt.sh

### A. Via Website

Buka **https://crt.sh** dan masukkan domain target.

**Query dasar:**
```
%.target.com
```
Gunakan wildcard `%` (seperti `*` di SQL) untuk mencari semua subdomain. Contoh:
```
https://crt.sh/?q=%25.example.com
```
URL-encoded: `%25` = `%`

### B. Via API (curl)

crt.sh memiliki API sederhana yang mengembalikan JSON:

**Mencari sertifikat untuk suatu domain:**
```bash
curl -s 'https://crt.sh/?q=example.com&output=json'
```

**Dengan wildcard:**
```bash
curl -s 'https://crt.sh/?q=%25.example.com&output=json'
```

**Membatasi hasil dengan exclude expired:**
```bash
curl -s 'https://crt.sh/?q=%25.example.com&output=json&exclude=expired'
```

**Identity match — hanya sertifikat yang CN/SAN-nya PERSIS domain:**
```bash
curl -s 'https://crt.sh/?q=example.com&output=json&match=LIKE'
```

### C. Filter Lanjutan

| Parameter | Fungsi |
|-----------|--------|
| `?q=` | Query pencarian (domain/CN/SAN) |
| `&output=json` | Output JSON |
| `&exclude=expired` | Hanya sertifikat valid |
| `&deduplicate=Y` | Hapus duplikat berdasarkan fingerprint |
| `&match=LIKE` | Exact match (tanpa wildcard implisit) |
| `&limit=N` | Batasi jumlah hasil (default 1000) |

## 4. Alur Kerja (Workflow) Lengkap untuk Pentesting

### Phase 1: Reconnaissance Pasif

```bash
# Step 1 — Ambil semua subdomain dari crt.sh
curl -s 'https://crt.sh/?q=%25.target.com&output=json' | jq -r '.[].name_value' | sort -u > crtsh_subdomains.txt

# Step 2 — Bersihkan hasil (hapus wildcard dan newlines)
cat crtsh_subdomains.txt | sed 's/\*\.//g' | tr ',' '\n' | sort -u > cleaned_subdomains.txt

# Step 3 — Filter domain yang valid
cat cleaned_subdomains.txt | grep -E '^([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$' > valid_subdomains.txt
```

### Phase 2: Enrichment & Validasi

```bash
# Step 4 — Cek resolusi DNS
while read sub; do
  host "$sub" 2>/dev/null | grep "has address" | awk '{print $1, $4}'
done < valid_subdomains.txt > resolved_hosts.txt

# Step 5 — Cek HTTP/HTTPS status
cat valid_subdomains.txt | httpx -silent -status-code -title -tech-detect -o live_hosts.txt
```

### Phase 3: Analisis Mendalam

```bash
# Step 6 — Ekstrak informasi spesifik dari crt.sh
curl -s 'https://crt.sh/?q=%25.target.com&output=json' | \
  jq -r '.[] | "\(.id) | \(.name_value) | \(.issuer_name) | \(.not_before) | \(.not_after) | \(.serial_number)"' \
  > cert_details.txt

# Step 7 — Cari sertifikat expired (yang terlewat renew)
curl -s 'https://crt.sh/?q=%25.target.com&output=json' | \
  jq -r '.[] | select(.not_after < now) | .name_value' | sort -u
```

## 5. Tips & Trick

### Tip 1: Gunakan `jq` untuk Parse JSON Efisien

```bash
# Ambil hanya SAN, unik, tanpa wildcard
curl -s 'https://crt.sh/?q=%25.target.com&output=json' | \
  jq -r '.[].name_value' | sed 's/\*\.//g' | tr ',' '\n' | sort -u
```

### Tip 2: Deduplikasi Berdasarkan Fingerprint

```bash
curl -s 'https://crt.sh/?q=%25.target.com&output=json' | \
  jq -r 'unique_by(.fingerprint) | .[].name_value' | \
  sed 's/\*\.//g' | tr ',' '\n' | sort -u
```

### Tip 3: Kombinasi dengan Tools Lain

```bash
# crt.sh → subfinder → httpx → nuclei
curl -s 'https://crt.sh/?q=%25.target.com&output=json' | \
  jq -r '.[].name_value' | sed 's/\*\.//g' | tr ',' '\n' | sort -u | \
  subfinder -silent | httpx -silent | nuclei -t ~/nuclei-templates/
```

### Tip 4: Identity Match (Exact Domain Only)

Gunakan `&match=LIKE` untuk hanya mengambil sertifikat yang CN/SAN-nya **persis** domain yang dicari. Berguna saat ingin menghindari noise dari wildcard atau subdomain tidak terkait.

### Tip 5: Format Output untuk Tools Lain

```bash
# Format untuk masscan/nmap
curl -s 'https://crt.sh/?q=%25.target.com&output=json' | \
  jq -r '.[].name_value' | sed 's/\*\.//g' | tr ',' '\n' | sort -u | \
  while read d; do echo "$d:443"; done > targets.txt
```

### Tip 6: Cari Subdomain Tersembunyi via SAN

Seringkali subdomain yang tidak terdaftar di DNS manapun tetap muncul di CT log karena sertifikatnya pernah diterbitkan. Ini adalah cara menemukan **staging**, **dev**, **admin**, atau **internal** subdomain.

### Tip 7: Cek Perubahan Sertifikat dari Waktu ke Waktu

```bash
# Bandingkan hasil crt.sh hari ini vs kemarin
curl -s 'https://crt.sh/?q=%25.target.com&output=json' > today.json
diff <(cat yesterday.json | jq -r '.[].name_value' | sort -u) \
     <(cat today.json | jq -r '.[].name_value' | sort -u)
```

### Tip 8: Gunakan `crtsh` Python Library

```bash
pip install crtsh
```

```python
from crtsh import crtsh
domains = crtsh("target.com")
for d in domains:
    print(d['name_value'])
```

## 6. Cheatsheet Lengkap

### API Query

| Tujuan | Command |
|--------|---------|
| Semua subdomain (wildcard) | `curl -s 'https://crt.sh/?q=%25.target.com&output=json'` |
| Exact match saja | `curl -s 'https://crt.sh/?q=target.com&output=json&match=LIKE'` |
| Hanya sertifikat valid | `curl -s 'https://crt.sh/?q=%25.target.com&output=json&exclude=expired'` |
| Deduplikasi otomatis | `curl -s 'https://crt.sh/?q=%25.target.com&output=json&deduplicate=Y'` |
| Batasi jumlah hasil | `curl -s 'https://crt.sh/?q=%25.target.com&output=json&limit=100'` |

### Parsing & Filtering

| Tujuan | Command |
|--------|---------|
| Ambil semua domain unik | `jq -r '.[].name_value' \| sed 's/\*\.//g' \| tr ',' '\n' \| sort -u` |
| Ambil semua issuer name | `jq -r '.[].issuer_name' \| sort -u` |
| Cari sertifikat wildcard | `jq -r '.[].name_value' \| grep '^\*\.' \| sort -u` |
| Cari sertifikat expired | `jq -r '.[] \| select(.not_after < now) \| .name_value'` |
| Cari by issuer tertentu | `jq -r '.[] \| select(.issuer_name \| contains("Let\'s Encrypt")) \| .name_value'` |
| Format untuk nmap/httpx | `sed 's/^/https:\/\//' \| sort -u` |
| Hitung total subdomain | `wc -l` |
| Sort by expiry date | `jq -r '.[] \| "\(.not_after) \(.name_value)"' \| sort` |

### One-liner Power Commands

```bash
# Complete recon pipeline
curl -s "https://crt.sh/?q=%25.$TARGET&output=json" | \
  jq -r '.[].name_value' | \
  sed 's/\*\.//g' | \
  tr ',' '\n' | \
  sort -u | \
  httpx -silent -status-code -title | \
  tee -a live_targets.txt

# Cari subdomain yang tidak terresolve DNS (shadow subdomains)
curl -s "https://crt.sh/?q=%25.$TARGET&output=json" | \
  jq -r '.[].name_value' | \
  sed 's/\*\.//g' | \
  tr ',' '\n' | \
  sort -u | \
  while read d; do
    host "$d" 2>/dev/null | grep -q "has address" || echo "$d [NO DNS]"
  done > shadow_domains.txt
```

## 7. Keterbatasan crt.sh

1. **Tidak semua domain tercatat** — Domain yang tidak menggunakan HTTPS tidak akan muncul.
2. **Wildcard certificate** — Satu sertifikat wildcard (`*.target.com`) mencakup banyak subdomain, tapi tidak mencakup domain non-wildcard yang spesifik.
3. **Rate limiting** — Query terlalu banyak dalam waktu singkat bisa kena batasan.
4. **Data historis terbatas** — CT log bersifat append-only; sertifikat yang di-revoke tetap muncul.
5. **Delay** — Ada jeda antara penerbitan sertifikat dan munculnya di crt.sh (biasanya beberapa menit hingga beberapa jam).

## 8. Kesimpulan

crt.sh adalah **sumber reconnaissance pasif terbaik** untuk menemukan subdomain, memahami infrastruktur SSL/TLS target, dan mengidentifikasi potensi vektor serangan — **tanpa menyentuh server target sama sekali**. Teknik yang digunakan Netcraft hanyalah salah satu dari banyak kemungkinan pengolahan data CT log.

Kombinasikan crt.sh dengan tools seperti `subfinder`, `httpx`, `nuclei`, dan `amass` untuk hasil maksimal dalam engagement penetration testing Anda.

Tentu, banyak tools dan script yang mengintegrasikan crt.sh sebagai bagian dari pipeline reconnaissance mereka. Berikut daftar lengkapnya:
# Tools
## 1. Tools CLI Khusus crt.sh

### crtsh (Python CLI)
```bash
pip install crtsh

# Penggunaan
crtsh -d target.com
crtsh -d target.com --output json
crtsh -d target.com --expired  # Include expired certificates
```

## 2. Tools Reconnaissance Umum dengan Integrasi crt.sh

### **Subfinder** (ProjectDiscovery) — ⭐ Paling Populer
```bash
# Install
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Dengan crt.sh
subfinder -d target.com -sources crtsh

# Default sudah include crt.sh
subfinder -d target.com

# Hanya dari crt.sh
subfinder -d target.com -sources crtsh -all
```
Subfinder menggunakan crt.sh sebagai salah satu dari 30+ sumber, dan hasilnya sangat optimal karena sudah handle deduplikasi dan parsing SAN.

### **Amass** (OWASP)
```bash
# Install
go install -v github.com/owasp-amass/amass/v4/...@master

# Amass otomatis menggunakan CT logs termasuk crt.sh
amass enum -d target.com

# Untuk memaksa hanya dari CT sources
amass enum -d target.com -config config.ini
# Dalam config.ini: sources = crt
```
Amass menggunakan **Certificate Transparency** sebagai data source, termasuk crt.sh, Google CT, Facebook CT, dan lainnya.

### **Assetfinder** (Tomnomnom)
```bash
# Install
go install github.com/tomnomnom/assetfinder@latest

# Assetfinder menggunakan crt.sh secara default
assetfinder --subs-only target.com

# Untuk certspotter/crtsh saja
assetfinder target.com | grep -E "\.target\.com"
```

### **Findomain**
```bash
# Install
wget https://github.com/Findomain/Findomain/releases/latest/download/findomain-linux.zip

# Dengan API key crt.sh
findomain -t target.com -a

# Tanpa API key (tetap include crt.sh)
findomain -t target.com
```

## 3. Tools OSINT Framework

### **TheHarvester**
```bash
git clone https://github.com/laramies/theHarvester.git
cd theHarvester

# Menggunakan crt.sh sebagai source
python3 theHarvester.py -d target.com -b crtsh
```
TheHarvester bisa mengambil data dari crt.sh untuk menemukan subdomain dan alamat email.

### **Recon-ng**
```bash
# Di dalam recon-ng console
marketplace install recon/domains-hosts/certificate_transparency
marketplace install recon/domains-hosts/certspotter

# Jalankan
use recon/domains-hosts/certificate_transparency
set SOURCE target.com
run
```

## 4. Script & One-liner Kustom

### **Bash Script Lengkap (crt_recon.sh)**
```bash
#!/bin/bash
# crt_recon.sh — Full recon pipeline

TARGET=$1
OUTPUT_DIR="crt_recon_$TARGET"
mkdir -p $OUTPUT_DIR

echo "[+] Fetching certificates from crt.sh..."
curl -s "https://crt.sh/?q=%25.$TARGET&output=json" | \
  jq -r '.[].name_value' | \
  sed 's/\*\.//g' | \
  tr ',' '\n' | \
  sort -u > $OUTPUT_DIR/raw_subdomains.txt

echo "[+] Filtering valid domains..."
grep -E '^([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$' \
  $OUTPUT_DIR/raw_subdomains.txt > $OUTPUT_DIR/valid_subdomains.txt

echo "[+] Checking live hosts..."
cat $OUTPUT_DIR/valid_subdomains.txt | \
  httpx -silent -status-code -title -tech-detect \
  -o $OUTPUT_DIR/live_hosts.txt

echo "[+] Results saved in $OUTPUT_DIR/"
```

### **Python Script Kustom**
```python
#!/usr/bin/env python3
# crt_scraper.py

import requests
import json
import sys

def get_crtsh_domains(domain):
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        data = resp.json()
        
        domains = set()
        for cert in data:
            name = cert.get('name_value', '')
            # Handle multiple SAN separated by newline
            for d in name.split('\n'):
                d = d.strip().replace('*.', '')
                if d and domain in d:
                    domains.add(d)
        return sorted(domains)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 crt_scraper.py target.com")
        sys.exit(1)
    
    domains = get_crtsh_domains(sys.argv[1])
    for d in domains:
        print(d)
```

## 5. Tools Web & GUI

### **Netcraft Site Report** (https://sitereport.netcraft.com)
- Menggunakan crt.sh di backend untuk menampilkan riwayat sertifikat
- Gratis untuk basic report

### **SecurityTrails** (https://securitytrails.com)
- Integrasi CT logs termasuk crt.sh
- API berbayar, tapi free tier ada
```bash
curl -s "https://api.securitytrails.com/v1/domain/target.com/subdomains" \
  -H "APIKEY: YOUR_KEY"
```

### **Censys** (https://censys.io)
- Menggunakan CT logs sebagai salah satu sumber
```bash
# Via Censys CLI
censys search "services.tls.certificates.leaf_data.subject.common_name: *.target.com"
```

### **Shodan** (https://shodan.io)
- Menggunakan data CT untuk enrichment
```bash
shodan search "ssl.cert.subject.cn:*target.com"
```

## 6. Tool Comparison Matrix

| Tool | Sumber crt.sh | Output | Kecepatan | Fitur Spesial |
|------|--------------|--------|-----------|---------------|
| **Subfinder** | ✅ Default | Domain list | ⚡ Sangat Cepat | Multi-source, output JSON |
| **Amass** | ✅ Default | Domain + Graph data | 🐢 Lambat | Graph visualization, API integration |
| **Assetfinder** | ✅ Default | Domain list | ⚡ Cepat | Simple, minimal dependencies |
| **Findomain** | ✅ Configurable | Domain list | ⚡ Sangat Cepat | Multi-threaded, API key support |
| **TheHarvester** | ✅ Sebagai source | Domain + Emails | 🐢 Sedang | Email discovery juga |
| **Recon-ng** | ✅ Module-based | Domain list | 🐢 Sedang | Modular, report generation |
| **crt.sh CLI** | ✅ Dedicated | Domain list + Detail | ⚡ Cepat | Cert detail, expired filter |

## 7. Cheatsheet Penggunaan Cepat

```bash
# === Subfinder (Rekomendasi #1) ===
subfinder -d target.com -silent | tee subs.txt
subfinder -d target.com -sources crtsh -all -silent
subfinder -d target.com -recursive -silent

# === Amass ===
amass enum -d target.com -o subs.txt
amass enum -d target.com -config config.ini -o subs.txt

# === Assetfinder ===
assetfinder --subs-only target.com | tee subs.txt

# === Findomain ===
findomain -t target.com -o
findomain -t target.com -q -u subs.txt

# === TheHarvester ===
theHarvester -d target.com -b crtsh -l 500

# === Pipeline Lengkap (Best Practice) ===
subfinder -d target.com -silent | \
  httpx -silent -status-code -title | \
  nuclei -t ~/nuclei-templates/ -o vulns.txt
```

**Kesimpulan:** Tools yang paling recommended adalah **Subfinder** karena kecepatan, akurasi, dan kemudahan integrasi dengan tools ProjectDiscovery lainnya (httpx, nuclei, katana). Jika butuh analisis lebih dalam tentang riwayat sertifikat, gunakan **crt.sh CLI + jq** secara langsung.

[Previously](02Netcraft.md) | [Next](../active/00Whois.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
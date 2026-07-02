# Shodan - Mesin Pencari untuk Perangkat yang Terhubung ke Internet

## 1. Apa itu Shodan?

**Shodan** (*search engine for the Internet of Everything*) adalah mesin pencari yang mengindeks perangkat yang terhubung ke internet, bukan halaman web seperti Google, melainkan **banner** (respons) dari protokol jaringan seperti HTTP, SSH, FTP, Telnet, SNMP, RTSP, kamera IP, PLC industri, dan ribuan port/services lainnya.

Informasi yang diindeks Shodan meliputi:
- **Alamat IP** dan **port** yang terbuka
- **Banner layanan** (banner grabbing) - versi software, konfigurasi, pesan selamat datang
- **Metadata geolokasi** (negara, kota, koordinat, ISP, ASN)
- **Vulnerability info** - CVE yang terasosiasi dengan versi software tertentu
- **Screenshots** - untuk layanan HTTP, VNC, RTSP, kamera

## 2. Teknik yang Digunakan Shodan

### a. **Port Scanning Massal**
Shodan secara kontinu memindai seluruh IPv4 publik di internet. Tidak seperti Nmap yang memindai satu host, Shodan memindai seluruh range IP untuk port-port tertentu secara periodik.

### b. **Banner Grabbing**
Ketika sebuah port terbuka ditemukan, Shodan mengirimkan request (sesuai protokol) dan membaca **banner** yang dikembalikan oleh server. Contoh:
- **HTTP**: Mengirim `GET / HTTP/1.0` → membaca header `Server`, `X-Powered-By`, dll.
- **SSH**: Membaca string identifikasi seperti `SSH-2.0-OpenSSH_8.9p1`
- **FTP**: Membaca banner seperti `220 ProFTPD 1.3.5 Server ready`

### c. **Parsing & Indexing**
Banner yang dikumpulkan di-*parse* menjadi field terstruktur (port, protocol, product, version, organization, location, timestamp, tags seperti `vuln`, `cloud`, `iot`, dll).

### d. **Geolokasi & ASN Lookup**
Setiap IP dicocokkan dengan database geolokasi (MaxMind) dan data WHOIS/ASN untuk mengetahui lokasi, penyedia layanan, dan organisasi pemilik.

### e. **Integrasi CVE (Vulnerability Mapping)**
Shodan mencocokkan versi produk yang terdeteksi dengan database kerentanan (NVD) dan menandai perangkat yang menjalankan versi rentan.

### f. **Shodan Honeypot Detection**
Shodan menandai IP yang diketahui sebagai honeypot (perangkap) agar pengguna dapat memfilternya.

### g. **Shodan Images & Screenshots**
Untuk protokol grafis (VNC, RDP, RTSP, HTTP), Shodan mengambil screenshot dari tampilan perangkat.

## 3. Cara Menggunakan Shodan

### A. **Melalui Website** (shodan.io) - *Free tier limited*

**Basic Search:**
- Masukkan query di kotak pencarian
- Hasil menampilkan IP, port, lokasi, dan banner

**Contoh query:**
```
apache
```
→ Semua perangkat dengan banner mengandung "apache"

```
port:22 country:JP
```
→ Host di Jepang dengan port SSH terbuka

### B. **Filter / Search Filters (Advanced Query)**

| Filter | Fungsi | Contoh |
|--------|--------|--------|
| `port:` | Port tertentu | `port:3389` |
| `country:` | Kode negara 2 huruf | `country:ID` |
| `city:` | Nama kota | `city:Jakarta` |
| `org:` | Nama organisasi/ISP | `org:"Telkom Indonesia"` |
| `hostname:` | Hostname/FQDN | `hostname:*.go.id` |
| `net:` | CIDR / subnet | `net:103.10.60.0/24` |
| `os:` | Sistem operasi | `os:"Windows 10"` |
| `product:` | Nama produk | `product:nginx` |
| `version:` | Versi produk | `version:2.4.49` |
| `vuln:` | CVE tertentu | `vuln:CVE-2024-27198` |
| `http.title:` | Judul halaman web | `http.title:"login"` |
| `http.status:` | HTTP status code | `http.status:200` |
| `ssl:` | Cert info / issuer | `ssl:"Let's Encrypt"` |
| `has_screenshot:` | Punya screenshot | `has_screenshot:true` |
| `before/after:` | Waktu indeks | `after:01/01/2025` |
| `tag:` | Tag khusus (vuln, iot, cloud) | `tag:vuln` |

**Contoh query kompleks:**
```
port:8080 country:ID product:Tomcat http.status:200
```
→ Semua server Apache Tomcat di Indonesia di port 8080 yang merespon HTTP 200

### C. **Melalui CLI - `shodan` command-line tool**

**Instalasi:**
```bash
pip install shodan
```
Set API key:
```bash
shodan init YOUR_API_KEY
```

**Perintah Dasar:**
```bash
# Cari host berdasarkan IP
shodan host <IP>

# Cari dengan query
shodan search --fields ip_str,port,org,country 'apache country:ID'

# Download hasil ke file
shodan download hasil-apache 'apache country:ID'

# Parse hasil download
shodan parse --fields ip_str,port hasil-apache.json.gz

# Statistik / ringkasan
shodan stats --facets port,country 'nginx'

# Cek IP saya
shodan myip

# Domain info
shodan domain example.com

# Alert (monitoring IP)
shodan alert create "monitor-web" 103.10.60.0/24
```

### D. **Melalui API / Python**

```python
import shodan

api = shodan.Shodan('YOUR_API_KEY')

# Cari
results = api.search('port:22 country:ID os:"Linux"')

for result in results['matches']:
    print(f"{result['ip_str']}:{result['port']} — {result.get('os','')}")

# Info host
host = api.host('8.8.8.8')
print(host)

# Statistik
facets = api.count('nginx', facets=[('port', 10)])
```

## 4. Alur Kerja (Workflow) Penggunaan Shodan

```
┌─────────────────────────────────────────────────────┐
│                    FASE 1: RECON                    │
│  ┌──────────────────────────────────────────────┐   │
│  │ Tentukan target:                             │   │
│  │ - Organisasi (org:"PT XYZ")                  │   │
│  │ - IP Range (net:103.10.60.0/24)              │   │
│  │ - Negara (country:ID)                        │   │
│  │ - Teknologi (product:Apache port:443)        │   │
│  └──────────────────────────────────────────────┘   │
│                          ↓                          │
│  ┌──────────────────────────────────────────────┐   │
│  │ Eksplorasi query:                            │   │
│  │ - Mulai broad → narrow                       │   │
│  │ - Gunakan facet untuk mapping port/product   │   │
│  │ - Export hasil ke CSV/JSON                   │   │
│  └──────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│             FASE 2: FILTERING & ANALISIS            │
│  ┌──────────────────────────────────────────────┐   │
│  │ Filter berdasarkan:                          │   │
│  │ - Versi rentan (vuln:CVE-xxxx)               │   │
│  │ - Default credentials                        │   │
│  │ - Screenshot menarik                         │   │
│  │ - Hostname mencurigakan                      │   │
│  └──────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│             FASE 3: TARGETING & VALIDASI            │
│  ┌──────────────────────────────────────────────┐   │
│  │ Periksa manual:                              │   │
│  │ - shodan host <IP> (banner detail)           │   │
│  │ - Buka di browser (HTTP/HTTPS)               │   │
│  │ - Nmap port scan tambahan                    │   │
│  │ - Test kerentanan (nmap --script vuln)       │   │
│  └──────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────┤
│            FASE 4: EKSPLOITASI & DOKUMENTASI        │
│  ┌──────────────────────────────────────────────┐   │
│  │ - Gunakan hasil validasi untuk eksploitasi   │   │
│  │ - Dokumentasikan temuan (IP, port, versi,    │   │
│  │   CVE, screenshot)                           │   │
│  │ - Rekomendasi remediasi                      │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## 5. Tips & Trik

### Query Optimization
- **Gunakan facet dulu** sebelum download: `shodan stats --facets port,product 'nginx country:ID'` untuk tahu distribusi port/product
- **Boolean logic**: Spasi = AND, `OR` bisa ditulis `||`, `NOT` = `-` (misal: `apache -nginx`)
- **Filter net dulu**, baru product - lebih cepat: `net:103.10.0.0/16 product:Apache`

### Recon Target Spesifik
- **Cari subdomain**: `hostname:*.example.com`
- **Cari cloud infra**: `org:"Amazon" port:443 country:ID`
- **Cari perangkat IoT**: `port:554` (RTSP), `port:23` (Telnet), `port:161` (SNMP)
- **Cari admin panel**: `http.title:"admin" http.status:200 -http.title:"404"`

### Security Perspective
- **Cari exposed database**: `product:MongoDB port:27017`, `product:Redis port:6379`, `product:Elasticsearch port:9200`
- **Cari default credential**: Filter `Authentication: disabled` atau banner yang menampilkan "default password"
- **Cari PLC/SCADA**: `port:502` (Modbus), `port:44818` (EtherNet/IP), tag: `tag:industrial`

### Performa
- **Gunakan `shodan download` + `shodan parse`** daripada search berulang (lebih cepat & hemat credit API)
- **Gunakan `--limit`** jika ingin membatasi hasil
- **Shodan Stream API** untuk data real-time (hanya untuk paid plan)

### Ekspor & Integrasi
- **Export ke format tools lain**: JSON → parse dengan jq → masukkan ke Nmap, Metasploit, Burp Suite
- **Bash oneliner:**
  ```bash
  shodan search --fields ip_str,port 'product:Apache country:ID' | awk 'NR>1 {print $1":"$2}' > targets.txt
  ```

## 6. Cheatsheet Ringkas

### 🔍 **Search Filters**

| Filter | Contoh |
|--------|--------|
| `country:` | `country:ID` |
| `city:` | `city:Jakarta` |
| `port:` | `port:22` |
| `net:` | `net:103.10.60.0/24` |
| `org:` | `org:"Telkom"` |
| `hostname:` | `hostname:*.ac.id` |
| `os:` | `os:"Linux 2.6.x"` |
| `product:` | `product:nginx` |
| `version:` | `version:1.18.0` |
| `vuln:` | `vuln:CVE-2021-41773` |
| `tag:` | `tag:vuln`, `tag:iot`, `tag:cloud` |
| `http.title:` | `http.title:"Login"` |
| `http.status:` | `http.status:200` |
| `ssl:` | `ssl:"Let's Encrypt"` |
| `has_screenshot:` | `has_screenshot:true` |
| `after/before:` | `after:01/06/2025` |

### 🖥️ **CLI Commands**

```bash
# Info host
shodan host <IP>

# Pencarian + export fields
shodan search --fields ip_str,port,org,country,os,hostnames '<query>'

# Download massive data
shodan download <filename> '<query>'

# Parse hasil download
shodan parse --fields ip_str,port,org <filename>.json.gz

# Statistik
shodan stats --facets port,product,country '<query>'

# Alert / monitoring
shodan alert create <nama> <CIDR>
shodan alert list
shodan alert info <id>
shodan alert delete <id>
```

### **Python Quick Reference**

```python
import shodan
api = shodan.Shodan('API_KEY')

# Search
r = api.search('product:nginx country:ID', limit=100)
for m in r['matches']:
    print(m['ip_str'], m['port'])

# Host info
h = api.host('1.2.3.4')

# Count
c = api.count('port:21', facets=[('country', 5)])

# Alert
api.create_alert('alert1', ['103.10.60.0/24'])
alerts = api.alerts()
```

### **Common Recon Queries**

```
# Kamera IP terbuka
has_screenshot:true port:554 country:ID

# RDP exposed
port:3389 country:ID os:"Windows"

# SSH with old version
port:22 product:OpenSSH version:7.2 country:ID

# Database tidak terproteksi
product:"MongoDB" port:27017 -authentication
product:"Redis" port:6379

# PLC / SCADA
port:502 country:ID
port:44818 country:ID

# Web server out-of-date
product:Apache version:2.4.49 country:ID
product:nginx version:1.18.0

# Admin panel / login page
http.title:"Admin" http.status:200
http.title:"Dashboard" port:8080

# SSL expired / problematic
ssl.cert.expired:true
```

## Catatan Etis & Legal

Shodan adalah alat **OSINT (Open Source Intelligence)** semua data yang diindeks adalah informasi publik yang dikirim oleh perangkat itu sendiri ke internet. Namun demikian, **akses dan pengujian terhadap perangkat yang terindeks tanpa izin adalah ilegal** di hampir semua yurisdiksi. Gunakan Shodan hanya untuk:
- **Security assessment** terhadap aset yang Anda miliki
- **Bug bounty** pada program yang sah
- **Penetration testing** dengan izin tertulis
- **Research akademik** yang etis
- **OSINT / threat intelligence** untuk pertahanan

[Previously](../../04Information-Gathering.md) | [Next](01GDorking.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
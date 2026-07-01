
# Netcraft

## Apa Itu Netcraft?

**Netcraft** adalah platform layanan keamanan siber dan analisis infrastruktur internet yang berbasis di Bath, Inggris. Bagi seorang penetration tester, Netcraft adalah **OSINT powerhouse** - alat untuk memetakan infrastruktur target, mengidentifikasi teknologi yang digunakan, menemukan subdomain, dan mengungkap relasi antar server tanpa perlu menyentuh target secara langsung.

Netcraft terkenal dengan **layanan "What's that site running?"** yang bisa mengungkap *stack teknologi* sebuah website hanya dari URL.
## Teknik-Teknik yang Digunakan Netcraft

### 1. **DNS Enumeration & Zone Transfer**
Netcraft mengumpulkan data dari query DNS publik, termasuk mencoba *zone transfer* (AXFR) — teknik yang jarang berhasil tapi sangat berharga jika server DNS target miskonfigurasi.

### 2. **HTTP Header Fingerprinting**
Dengan mengirim request HTTP ke server target, Netcraft menganalisis header respons seperti:
- `Server` → mengungkap Apache, Nginx, IIS, dll.
- `X-Powered-By` → mengungkap PHP, ASP.NET, dll.
- `Set-Cookie` → mengungkap session handling dan backend framework.

### 3. **SSL/TLS Certificate Transparency Log Analysis**
Netcraft memindai database **Certificate Transparency (CT) logs** untuk menemukan sertifikat SSL yang diterbitkan untuk domain target — termasuk subdomain tersembunyi.

### 4. **Active Web Crawling & Site Relationship Graph**
Netcraft secara aktif merayapi website target dan menganalisis tautan, IP address, dan relasi antar domain untuk membangun peta infrastruktur.

### 5. **BGP & IP Netblock Analysis**
Netcraft melacak kepemilikan IP (ASN, netblock) untuk mengidentifikasi semua server yang berjalan pada infrastruktur yang sama — bahkan jika server tersebut tidak terhubung langsung ke domain utama.

## Cara Menggunakan Netcraft

### A. **Melalui Website (free)**
- [https://www.netcraft.com](https://www.netcraft.com)
- [https://sitereport.netcraft.com/](https://sitereport.netcraft.com/)

**Langkah:**
1. Buka **Netcraft Toolbar** atau langsung ke halaman *"What's that site running?"*
2. Masukkan URL target: `https://target.com`
3. Netcraft akan menampilkan:
   - **OS & Web Server** → misal: Linux, Apache/2.4.41
   - **Uptime History** → mengetahui kapan terakhir restart server
   - **IP Address** & **Netblock Owner**
   - **DNS Servers** → NS record resolver
   - **Site Technology** → bahasa pemrograman, framework JS, CDN

### B. **Netcraft Extension (Browser)**

Install ekstensi Netcraft untuk Firefox/Chrome. Saat browsing, ekstensi ini bisa menampilkan informasi keamanan dan teknologi dari setiap situs yang dikunjungi.

### C. **Netcraft API (untuk automation)**

Netcraft menyediakan API berbayar untuk query otomatis. Cocok untuk integrasi dengan tool pentest lain.

## Alur Kerja Netcraft dalam Penetration Testing

```
┌──────────────────────────────────────────────────────────┐
│                  INPUT: Domain Target                    │
│                    (target.com)                          │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│               1. DNS LOOKUP & ENUMERATION                │
│   - A, AAAA, MX, NS, TXT, SOA records                    │
│   - Coba zone transfer (AXFR)                            │
│   - Hasil: IP server, mail server, nameserver            │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│             2. SSL/TLS CERTIFICATE ANALYSIS              │
│   - Scan CT Logs untuk subdomain                         │
│   - Dapatkan: semua domain dalam SAN certificate         │
│   - Hasil: subdomain tersembunyi                         │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│          3. HTTP REQUEST & HEADER ANALYSIS               │
│   - Request ke port 80, 443                              │
│   - Analisis Server, X-Powered-By, Cookies               │
│   - Hasil: web server, bahasa pemrograman, framework     │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│          4. INFRASTRUCTURE MAPPING                       │
│   - IP geolocation, ASN, netblock                        │
│   - Cari semua domain di netblock yang sama              │
│   - Hasil: footprint infrastruktur                       │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│             5. UPTIME & HISTORY ANALYSIS                 │
│   - Lihat pola restart server                            │
│   - Tracking perubahan IP, web server                    │
│   - Hasil: pola maintenance, celah waktu eksploitasi     │
└─────────────────────────┬────────────────────────────────┘
                          ▼
┌──────────────────────────────────────────────────────────┐
│            6. CORRELATION & REPORTING                    │
│   - Gabungkan dengan data OSINT lain (Shodan, Censys)    │
│   - Buat attack surface map                              │
│   - Dokumentasi untuk laporan pentest                    │
└──────────────────────────────────────────────────────────┘
```

## Tips & Trick

### 1. **Cari Subdomain via CT Logs Secara Manual**
Netcraft menampilkan subdomain dari CT logs. Manfaatkan untuk menemukan:
- `dev.target.com`
- `staging.target.com`
- `admin.target.com`
- `jenkins.target.com`
- `vpn.target.com`

### 2. **Gunakan Netcraft + Shodan untuk Validasi**
IP yang ditemukan Netcraft, cross-check di Shodan untuk melihat port terbuka, service banner, dan CVE potensial.

### 3. **Analisis Uptime History untuk Mendeteksi Patch Cycle**
Jika server restart setiap hari Minggu pukul 02:00 — itu jadwal maintenance. Serang di luar jadwal itu atau exploit sebelum patch diterapkan.

### 4. **Identifikasi Shared Hosting**
Netcraft bisa menunjukkan bahwa IP target digunakan oleh puluhan domain lain. Jika shared hosting, cari domain lain di IP yang sama yang mungkin lebih lemah.

### 5. **Perhatikan Perubahan Teknologi**
Netcraft menyimpan history teknologi. Jika target berpindah dari Apache ke Nginx atau dari PHP ke Node.js — itu tanda migrasi infrastruktur yang mungkin menyisakan celah.

### 6. **Find Related Sites**
Gunakan fitur "Find other sites on the same IP address" untuk memperluas permukaan serangan.

### 7. **Cek SSL Chain Expiry**
Netcraft menampilkan tanggal expiry sertifikat. Sertifikat yang hampir kadaluarsa bisa menandakan admin yang lalai.

## Cheatsheet Cepat

| **Tujuan** | **Yang Dicari di Netcraft** | **Gunakan Untuk** |
|---|---|---|
| Web server fingerprinting | Site Report → "Web Server" | Tentukan exploit yang cocok |
| Subdomain discovery | "SSL Certificate" → SAN list | Temukan admin panel, dev server |
| Infrastruktur mapping | "Netblock Owner" | Cari semua domain dalam netblock |
| Shared hosting detection | "Sites on this IP" | Lompat ke target lain di IP yang sama |
| Teknologi stack | "Site Technology" | Ketahui framework, bahasa, CDN |
| History & pattern | "Uptime Graph" | Analisis maintenance window |
| Mail server discovery | DNS → "Mail Servers (MX)" | Target untuk SMTP enumeration |
| Nameserver discovery | DNS → "Nameservers (NS)" | Coba zone transfer attack |
| IP geolocation | "IP Address" → Geo | Batasi scope geografis |
| Cloud/CDN detection | "Site Technology" → Cloud | Bypass WAF atau CDN |

## Contoh Penggunaan Langsung

**Target:** `https://example-bank.com`

1. Buka Netcraft → masukkan URL → dapat:
   - **IP:** `203.0.113.50` (milik AWS)
   - **Web Server:** nginx/1.18.0
   - **Framework:** React, Node.js
   - **SAN Certificate:** `example-bank.com`, `*.example-bank.com`, `admin.example-bank.com`
   - **Netblock:** AWS us-east-1 (54.0.0.0/8)

2. Subdomain ditemukan: `admin.example-bank.com`, `api.example-bank.com`, `dev.example-bank.com`

3. Cross-check `admin.example-bank.com` di Netcraft → dapat informasi berbeda (Apache/2.4.41, PHP 7.4) — berarti server terpisah, attack surface baru.

4. Cek "Sites on this IP" → 15 domain lain di IP yang sama, beberapa mungkin tidak seketat bank.

Ini **recon passif murni** — target tidak pernah tahu bahwa infrastruktur mereka sedang dipetakan.

## Script
- [Netcraft-Lite.py](../../script/Netcraft/index.md)

[Previously](01GDorking.md) | [Next](../active/00Whois.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
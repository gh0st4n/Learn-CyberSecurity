# Google Dorking (Google Hacking)

## Apa itu Google Dorking?

Google Dorking adalah teknik pencarian tingkat lanjut menggunakan **query khusus (dork)** pada mesin pencari Google untuk menemukan informasi sensitif yang tidak sengaja terekspos ke publik. Informasi ini bisa berupa file konfigurasi, database, log, kredensial, direktori yang tidak terproteksi, dan lain-lain.

Teknik ini memanfaatkan **operator pencarian Google** (seperti `site:`, `filetype:`, `intitle:`) untuk mempersempit hasil pencarian ke target spesifik.

## Operator Google Dorking Utama

| Operator    | Fungsi                                       | Contoh                            |
| ----------- | -------------------------------------------- | --------------------------------- |
| `site:`     | Membatasi pencarian ke domain tertentu       | `site:example.com`                |
| `filetype:` | Mencari tipe file tertentu                   | `filetype:pdf`                    |
| `intitle:`  | Mencari kata dalam judul halaman             | `intitle:"index of"`              |
| `inurl:`    | Mencari kata dalam URL                       | `inurl:wp-admin`                  |
| `intext:`   | Mencari kata dalam konten halaman            | `intext:password`                 |
| `cache:`    | Menampilkan versi cache halaman              | `cache:example.com`               |
| `link:`     | Mencari halaman yang me-link ke URL tertentu | `link:example.com`                |
| `"..."`     | Mencari frase persis (exact match)           | `"admin password"`                |
| `-`         | Mengecualikan kata                           | `site:example.com -filetype:html` |
| `*`         | Wildcard                                     | `"admin * password"`              |
| `\|`        | Atau (OR)                                    | `password \| passwd \| pass`      |

## Teknik Google Dorking Umum

### 1. **Menemukan Direktori Terbuka (Directory Listing)**
```
intitle:"index of" site:target.com
```
```
intitle:"index of /" "parent directory" site:target.com
```

### 2. **Mencari File Konfigurasi Sensitif**
```
filetype:env "DB_PASSWORD" site:target.com
```
```
filetype:conf "root" "password" site:target.com
```
```
filetype:sql "INSERT INTO" "password" site:target.com
```

### 3. **Mencari Kredensial & Data Login**
```
inurl:"login.php" "username" "password" site:target.com
```
```
filetype:log "username" "password" site:target.com
```
```
intext:"password" filetype:xlsx site:target.com
```

### 4. **Eksposur Database & Backup**
```
filetype:sql "MySQL dump" site:target.com
```
```
filetype:bak "password" site:target.com
```
```
inurl:backup filetype:zip site:target.com
```

### 5. **Panel Admin & CMS**
```
inurl:admin intitle:login site:target.com
```
```
inurl:wp-admin site:target.com
```
```
inurl:/administrator site:target.com
```

### 6. **Mencari Log & File Debug**
```
filetype:log "PHP Fatal error" site:target.com
```
```
filetype:log "GET /" "HTTP/1.1" site:target.com
```

### 7. **Deteksi Vulnerability (CVE)**
```
inurl:"?id=" "SQL" site:target.com
```
```
inurl:".php?cmd=" site:target.com
```

## Alur Kerja Google Dorking

```
1. Tentukan Target
   └─> Domain / IP Range / Nama Perusahaan

2. Pemetaan Awal (Reconnaissance)
   └─> site:target.com - Gunakan operator dasar

3. Identifikasi Teknologi
   └─> Cari file robots.txt, page source, header
   └─> Identifikasi CMS, web server, framework

4. Pencarian Dork Bertahap
   ├─> Lapisan 1: Directory listing, file backup
   ├─> Lapisan 2: File konfigurasi, env, log
   ├─> Lapisan 3: Kredensial, database dump
   └─> Lapisan 4: Panel admin, endpoint sensitif

5. Verifikasi Manual
   └─> Buka hasil yang menjanjikan
   └─> Validasi apakah informasi benar-benar ekspos

6. Dokumentasi & Pelaporan
   └─> Catat temuan, URL, tipe informasi
   └─> Rekomendasi mitigasi
```

## Mitigasi (Cara Melindungi Diri dari Google Dorking)

| Mitigasi | Penjelasan |
|----------|------------|
| **robots.txt** | Blok crawler dari direktori sensitif: `Disallow: /admin/` |
| **.htaccess / Nginx config** | Proteksi direktori dengan autentikasi |
| **NoIndex header** | Tambahkan `<meta name="robots" content="noindex">` |
| **Hapus file backup** | Jangan biarkan `file.bak`, `.old`, `.swp` di server |
| **Environment variables** | Jangan simpan kredensial di file `.env` yang terekspos |
| **Log rotation & protection** | Log jangan disimpan di `webroot` |
| **Review Google cache** | Cek `site:domain.com` secara berkala |

> **Catatan Penting:** Google Dorking hanya boleh dilakukan pada target yang **Anda miliki** atau telah mendapatkan **izin tertulis** untuk diuji. Penggunaan tanpa izin melanggar hukum dan termasuk aktivitas ilegal.

## Website, Script Python Sederhana & Cheatseet
- [ExploitDB GDork](https://www.exploit-db.com/google-hacking-database)
- [Script Simple Python](script/GDork/index.md)
- [GoogleDorking](script/GDork/GoogleDorking.md)

[Previously](00Shodan.md) | [Next](02Netcraft.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
# Penjelasan **Dirsearch**

**dirsearch** adalah tools *open-source* berbasis Python yang digunakan untuk **brute-force directory dan file enumeration** pada web server. Tujuannya adalah menemukan direktori, file, atau endpoint tersembunyi di target web aplikasi yang tidak terlihat dari navigasi normal.

## Teknik yang Digunakan

1. **Brute-force Dictionary-based Enumeration**  
   dirsearch menggunakan *wordlist* (kumpulan nama direktori dan file umum) lalu mencoba satu per satu pada target menggunakan HTTP request.

2. **Recursive Scanning**  
   Setelah menemukan direktori yang valid, dirsearch secara opsional bisa melanjutkan scanning ke dalam sub-direktori dari direktori tersebut secara rekursif.

3. **Multi-threading**  
   Mengirim banyak request secara paralel untuk mempercepat proses enumerasi.

4. **HTTP Status Code Filtering**  
   Membedakan respon berdasarkan status code:
   - `200 OK` → ditemukan
   - `301/302` → redirect (sering berarti direktori valid)
   - `403 Forbidden` → ada tapi tidak bisa diakses
   - `401 Unauthorized` → butuh autentikasi
   - `404` → tidak ditemukan (diabaikan)
   - `500` → error server

5. **Content-length / Response Size Filtering**  
   Menghilangkan *false positive* dengan membandingkan panjang respon bodi.

6. **Custom Headers & Authentication**  
   Mendukung penggunaan Cookie, Authorization header (Basic/Digest/NTLM/Bearer), dan User-Agent kustom.

7. **Extension Bruteforce**  
   Bisa mencoba berbagai ekstensi file secara otomatis (`.php`, `.asp`, `.txt`, `.bak`, `.zip`, `.git`, dll.) pada setiap entri wordlist.

## Cara Install 
### Via APT

```bash
sudo apt install dirsearch
```

### Via Git Clone

```bash
git clone https://github.com/maurosoria/dirsearch.git
cd dirsearch
```

**Dependencies** (Python 3.7+ wajib):

```bash
pip3 install -r requirements.txt
```

Atau langsung jalankan (`requirements.txt` akan di*check* otomatis):

```bash
python3 dirsearch.py
```

> **Catatan:** Tidak perlu `make` atau `configure`. dirsearch sudah siap pakai setelah clone dan install requirements.

## Cara Menggunakan

### 1. Basic Scan

```bash
python3 dirsearch.py -u https://target.com
```

### 2. Dengan Wordlist Kustom

```bash
python3 dirsearch.py -u https://target.com -w /path/to/wordlist.txt
```

### 3. Dengan Ekstensi File Spesifik

```bash
python3 dirsearch.py -u https://target.com -e php,asp,txt,zip,bak
```

### 4. Recursive Mode

```bash
python3 dirsearch.py -u https://target.com -r --deep-recursive
```

### 5. Multi-threading (kecepatan)

```bash
python3 dirsearch.py -u https://target.com -t 50
```

### 6. Menggunakan Cookie / Header

```bash
python3 dirsearch.py -u https://target.com --cookie "session=abc123"
python3 dirsearch.py -u https://target.com --header "X-Forwarded-For: 127.0.0.1"
```

### 7. Output ke File

```bash
python3 dirsearch.py -u https://target.com -o hasil.txt
```

### Parameter Penting Lainnya

| Parameter | Fungsi |
|-----------|--------|
| `-L` / `--url-list` | Scan dari file list URL |
| `--exclude-status` | Abaikan status code tertentu (misal: `--exclude-status 400,404`) |
| `--timeout` | Timeout per request (default: 5 detik) |
| `-x` | Abaikan status code (sama seperti `--exclude-status`) |
| `--full-url` | Tampilkan full URL di output |
| `--user-agent` | Kustom User-Agent |
| `--random-agent` | Gunakan User-Agent acak |

---

## Alur Kerja dirsearch

```
[1] START
     |
[2] Load Konfigurasi
     | - Baca target URL(s)
     | - Load wordlist file
     | - Set ekstensi (jika ada)
     | - Set thread, timeout, header, dll.
     |
[3] Pre-filtering Wordlist
     | - Generate kombinasi nama + ekstensi
     | - Buat antrian (queue) URL request
     |
[4] HTTP Request Loop (Multi-threaded)
     | - Kirim GET request ke setiap path
     | - Terima response (status code, headers, body)
     |
[5] Response Filtering
     | - Filter berdasarkan:
     |   • Status code (200, 301, 403, dll.)
     |   • Content-length (lawan false positive)
     |   • Redirect target
     |
[6] Output & Logging
     | - Tampilkan hasil di terminal (warna-warni)
     | - Simpan ke file output jika diminta
     |
[7] Recursive Check
     | - Jika mode recursive aktif & menemukan direktori:
     |   → Kembali ke step [3] dengan prefiks direktori baru
     |   → Scan sub-direktori secara otomatis
     |
[8] END (semua antrian habis)
     - Tampilkan summary: total ditemukan, total request, waktu tempuh
```

### Visual Sederhana Alurnya

```
Target URL + Wordlist
        │
        ▼
  ┌─────────────────┐
  │ Queue Generator │ => /admin, /admin/, /admin.php, /backup/, /backup.zip, ...
  └────────┬────────┘
           │
           ▼
  ┌──────────────────────┐
  │ Thread Pool (50 thd) │─── HTTP GET /admin ────→ Server ───→ 301 Redirect
  │                      │─── HTTP GET /backup ───→ Server ───→ 200 OK (12KB)
  │                      │─── HTTP GET /.git/ ─────→ Server ───→ 403 Forbidden
  │                      │─── HTTP GET /test ─────→ Server ───→ 404 Not Found
  └────────┬─────────────┘
           │
           ▼
  ┌─────────────────┐
  │ Response Filter │── 404 → discard
  │                 │── 200 → DISPLAY + LOG
  │                 │── 301 → follow / catat
  │                 │── 403 → catat (interesting)
  └────────┬────────┘
           │
           ▼
  ┌───────────────────┐
  │ Hasil ke Terminal │  /backup/ (200)   → [BACKUP FOLDER]
  │ + File Output     │  /admin/ (301)    → [ADMIN PANEL]
  │                   │  /.git/ (403)     → [INTERESTING]
  └───────────────────┘
```

## Contoh Kasus Penggunaan

```bash
# Scan cepat dengan default wordlist
python3 dirsearch.py -u http://testphp.vulnweb.com -e php

# Scan rekursif + simpan output
python3 dirsearch.py -u https://target.com -w /usr/share/wordlists/dirb/common.txt -r -o hasil.txt -t 30

# Scan dengan exclude 404 dan custom header
python3 dirsearch.py -u https://target.com --exclude-status 404,400 --header "Authorization: Bearer eyJ..."
```

## Kelebihan dirsearch

- **Cepat** - multi-threading dengan performa tinggi
- **Akurat** - filtering content-length mengurangi false positive
- **Fleksibel** - dukung berbagai ekstensi, header, metode autentikasi
- **Mature** - aktif dikembangkan sejak 2015, ribuan bintang di GitHub
- **Recursive out-of-the-box** - tanpa konfigurasi rumit

## Kekurangan

- Masih berbasis *wordlist* - tidak menemukan path yang tidak ada di wordlist
- Bisa membanjiri log server - perlu hati-hati pada target *production*
- Tidak built-in *spidering/crawling* seperti Feroxbuster (tapi bisa dikombinasikan)

[Previously](01Dirb.md) | [Next](03Dirhunt)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
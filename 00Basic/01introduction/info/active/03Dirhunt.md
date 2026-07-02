# Dirhunt - Web Directory Scanner & Crawler

## Apa itu Dirhunt?

**Dirhunt** adalah tools untuk menemukan hidden file, directory, dan endpoint pada web application. Berbeda dengan dirb atau gobuster yang brute-force dengan wordlist, **Dirhunt menggunakan teknik crawling cerdas** - dia menganalisis struktur halaman, URL relatif, JavaScript, dan pola umum untuk menemukan path tanpa perlu wordlist besar.

Tools ini dibuat oleh **Nekmo** dan ditulis dalam **Python 3**.

## Teknik yang Digunakan Dirhunt

Dirhunt menggunakan beberapa teknik sekaligus:

1. **Crawling Cerdas (Smart Crawling)** - Bukan brute-force buta. Dirhunt mengikuti link, membaca `href`, `src`, `action`, dan atribut lain dari HTML.

2. **Path Extraction dari JavaScript** - Mengekstrak path dan endpoint dari file `.js` yang ditemukan.

3. **Analisis Error Response** - Mendeteksi perbedaan response `404`, `403`, `200`, `301`, dan `500` untuk menyimpulkan apakah suatu path eksis atau tidak.

4. **Link Discovery Otomatis** - Menemukan path dari:
   - Anchor tags (`<a href="...">`)
   - Form actions (`<form action="...">`)
   - Script sources (`<script src="...">`)
   - Image sources (`<img src="...">`)
   - CSS/stylesheet links
   - Sitemap (`/sitemap.xml`)
   - `robots.txt`

1. **Recursive Scanning** - Setelah menemukan directory, Dirhunt akan otomatis masuk ke dalamnya dan melanjutkan scanning secara rekursif.

2. **Filtering & Pattern Matching** - Menerapkan pola umum directory naming (`admin`, `backup`, `uploads`, `api`, dll) untuk menebak path potensial.

## Perbandingan dengan Dirsearch

| Aspek | Dirhunt | Dirsearch |
|-------|---------|-----------|
| **Metode** | Crawling cerdas + analisis konten | Brute-force berbasis wordlist |
| **Kecepatan** | Lebih lambat per path, tapi lebih akurat | Sangat cepat dengan threading |
| **Wordlist** | Tidak perlu wordlist besar | Membutuhkan wordlist |
| **Cakupan** | Terbatas pada yang bisa di-crawl | Menyeluruh (semua path di wordlist) |
| **Recursive** | Otomatis | Opsional (dengan `-r`) |
| **Teknik utama** | Ekstraksi URL dari response HTML/JS | HTTP request massal |

> **Kombinasi ideal**: Gunakan Dirhunt untuk discovery awal (menemukan struktur aplikasi), lalu Dirsearch untuk brute-force depth path yang lebih dalam.

## Cara Install Dirhunt

### Opsi 1: Git Clone (Rekomendasi)

```bash
git clone https://github.com/Nekmo/dirhunt.git
cd dirhunt
pip install -r requirements.txt
pip install .
```

Atau langsung dengan setup:

```bash
git clone https://github.com/Nekmo/dirhunt.git
cd dirhunt
python setup.py install
```

### Opsi 2: Via pip

```bash
pip install dirhunt
```

### Opsi 3: Via uv (package manager Python modern)

```bash
# Install uv dulu jika belum punya
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dirhunt via uv
uv pip install dirhunt
```

Atau jika ingin menggunakan virtual environment dengan uv:

```bash
uv venv
uv pip install dirhunt
```

### Verifikasi Instalasi

```bash
dirhunt --help
```

## Cara Menggunakan Dirhunt

### Basic Usage

```bash
# Scan target dasar
dirhunt https://target.com

# Dengan output ke file
dirhunt https://target.com -o hasil.txt

# Simpan dalam format JSON
dirhunt https://target.com -o hasil.json --json
```

### Opsi Tambahan

```bash
# Tentukan user-agent custom
dirhunt https://target.com -u "Mozilla/5.0 ..."

# Set delay antar request (ms)
dirhunt https://target.com -d 500

# Maksimum kedalaman recursive
dirhunt https://target.com --max-depth 5

# Abaikan status code tertentu
dirhunt https://target.com --ignore 404

# Gunakan cookie/session
dirhunt https://target.com -c "PHPSESSID=abc123"

# Filter hanya status code tertentu
dirhunt https://target.com --filter 200,301,403

# Proxy (untuk Burp Suite)
dirhunt https://target.com -p http://127.0.0.1:8080

# Scan dengan thread
dirhunt https://target.com --threads 10
```

### Contoh Lengkap

```bash
dirhunt https://example.com -o scan_result.txt --json --threads 5 --max-depth 10 -p http://127.0.0.1:8080
```

---

## Alur Kerja (Workflow) Dirhunt

```
                    ┌──────────────────────┐
                    │   TARGET URL INPUT   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ 1. FETCH ROBOTS.TXT  │
                    │ 2. FETCH SITEMAP.XML │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ FETCH HOMEPAGE/URL  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌───────────────────────┐
                    │ PARSE HTML & EXTRACT: │
                    │ - <a href>            │
                    │ - <form action>       │
                    │ - <script src>        │
                    │ - <img src>           │
                    │ - <link href>         │
                    │ - JS file contents    │
                    └──────────┬────────────┘
                               │
                               ▼
                    ┌────────────────────────────┐
                    │ FILTER & NORMALIZE URLs:   │
                    │ - Remove duplicates        │
                    │ - Filter external domains  │
                    │ - Normalize path format    │
                    │ - Discard file extensions? │
                    └──────────┬─────────────────┘
                               │
                               ▼
                    ┌────────────────────────────┐
                    │ TEST EACH DISCOVERED PATH: │
                    │ - Kirim HTTP request       │
                    │ - Analisis response code   │
                    │ - Deteksi "fake 404"       │
                    └──────────┬─────────────────┘
                               │
                               ▼
               ┌────────────────────────────────┐
               │          VALID PATH?           │
               │    ┌──── YES ────┐  ┌── NO ──┐ │
               │    ▼             │  │        │ │
               │  Report Path     │  │  Skip  │ │
               │    │             │  │        │ │
               │    ▼             │  └────────┘ │
               │  Is Directory?───┘             │
               │    │       │                   │
               │   YES      NO                  │
               │    │       (file, skip)        │
               │    ▼                           │
               │  Recursive Crawl               │
               │  (masuk ke sub-directory)      │
               └────────────────────────────────┘
                               │
                               ▼
	                    ┌─────────────────┐
	                    │ REPORT HASIL:   │
	                    │ - Found paths   │
	                    │ - Status codes  │
	                    │ - Content types │
	                    │ - Response size │
	                    └─────────────────┘
```

### Penjelasan Detail Alur:

1. **Initial Fetch** - Pertama, Dirhunt mengambil `robots.txt` dan `sitemap.xml` untuk mendapatkan daftar path awal.

2. **Crawl Halaman Utama** - Halaman target di-fetch dan di-parse. Semua link, form, script, dan resource diekstrak.

3. **URL Extraction** - Path diekstrak dari berbagai sumber termasuk JavaScript (file `.js` di-crawl juga).

4. **Filtering & Normalisasi** - URL dinormalisasi (hapus query string, normalisasi path), duplikat dihapus, dan URL eksternal difilter.

5. **Path Testing** - Setiap path unik di-request untuk validasi. Dirhunt menggunakan teknik deteksi "soft 404" untuk membedakan halaman valid dari halaman error yang dikustomisasi.

6. **Recursive Crawling** - Jika suatu path adalah directory (mengembalikan 200/301 dengan konten directory listing atau halaman index), Dirhunt akan masuk ke dalamnya dan mengulang proses dari langkah 2.

7. **Reporting** - Semua path valid beserta metadata-nya (status code, content-type, response size) dicatat dan ditampilkan/diexport.

## Tips Penggunaan

- **Kombinasikan dengan Burp Suite**: Gunakan `-p http://127.0.0.1:8080` untuk mengarahkan traffic ke Burp dan memanfaatkan Repeater/Intruder.
- **Gunakan untuk recon awal**: Jalankan Dirhunt di awal pengujian untuk mapping struktur aplikasi sebelum menggunakan tools brute-force.
- **Simpan output JSON**: Format JSON memudahkan parsing untuk post-processing dengan script Python atau jq.
- **Pasang delay** jika target memiliki rate limiting (`-d 1000` untuk delay 1 detik).

[Previously](02Dirsearch.md) | [Next](04DNS.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
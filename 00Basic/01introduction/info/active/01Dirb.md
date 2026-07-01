
# Dirb - Web Content Scanner

**Dirb** adalah tools *web content scanner* yang digunakan untuk melakukan *brute-force directory* dan *file enumeration* pada web server. Tools ini bekerja dengan cara mengirimkan HTTP request ke target menggunakan wordlist, lalu menganalisis response code untuk menentukan apakah suatu direktori atau file ada atau tidak.
## Teknik yang Digunakan Dirb

| Teknik | Keterangan |
|---|---|
| **Dictionary-based Brute-force** | Menggunakan wordlist berisi nama direktori/file umum |
| **HTTP Response Code Analysis** | Membedakan kode respon (200 OK, 301 Redirect, 403 Forbidden, 404 Not Found, dll) |
| **Recursive Scanning** | Menelusuri direktori yang ditemukan untuk scan lebih lanjut |
| **Extension Bruteforce** | Mencoba berbagai ekstensi file (.php, .asp, .html, .txt, dll) |
| **Threading** | Multi-thread untuk mempercepat proses scanning |
## Cara Install Dirb

### Di Kali Linux (sudah pre-installed biasanya)

```bash
sudo apt update
sudo apt install dirb -y
```

### Install dari Source (opsional)

```bash
git clone https://salsa.debian.org/pkg-security-team/dirb
cd dirb
./configure
make
sudo make install
```

### Di macOS (via Homebrew)

```bash
brew install dirb
```
## Cara Menggunakan Dirb

### Basic Usage

```bash
dirb http://target.com/
```

### Dengan Wordlist Kustom

```bash
dirb http://target.com/ /usr/share/wordlists/dirb/common.txt
```

### Dengan Ekstensi File

```bash
dirb http://target.com/ -X .php,.html,.txt
```

### Recursive Scan

```bash
dirb http://target.com/ -r
```

### Non-Recursive (halaman utama saja)

```bash
dirb http://target.com/ -R
```

### Dengan User Agent Kustom

```bash
dirb http://target.com/ -a "Mozilla/5.0 (HackerAI)"
```

### Dengan Cookies

```bash
dirb http://target.com/ -c "session=abc123"
```

### Delay antar Request

```bash
dirb http://target.com/ -z 500
```

### Simpan Output ke File

```bash
dirb http://target.com/ -o hasil_scan.txt
```

### Menggunakan Proxy (misal Burp Suite)

```bash
dirb http://target.com/ -p http://127.0.0.1:8080
```
## Alur Kerja Dirb

```
[1] Input Target URL + Wordlist
            |
[2] Baca Wordlist (list direktori/file)
            |
[3] Loop setiap entry di wordlist:
    ├── Bentuk URL: http://target/direktori
    ├── Kirim HTTP Request
    ├── Analisis Response Code:
    │   ├── 200 → FOUND ✅ (direktori/file ada)
    │   ├── 301/302 → Redirect 🔄 (mungkin ada)
    │   ├── 403 → Forbidden 🔒 (ada tapi terlarang)
    │   └── 404 → Not Found ❌ (tidak ada)
    └── Jika recursive aktif → scan subdirektori
            |
[4] Tampilkan hasil ke terminal & simpan ke file
```
## Perbandingan Tools Sejenis

| Tools | Bahasa | Kelebihan |
|---|---|---|
| **Dirb** | C | Ringan, cepat, built-in di Kali |
| **Gobuster** | Go | Lebih cepat, support DNS & vhost |
| **Dirsearch** | Python | Banyak fitur, extension otomatis |
| **FFUF** | Go | Sangat cepat, fleksibel, modular |
| **SimpleDirb (script di atas)** | Python | Edukatif, mudah dimodifikasi |

Script Python di atas hanyalah versi sederhana untuk tujuan edukasi. Dirb asli memiliki banyak fitur lanjutan seperti *recursive scanning*, *cookie handling*, *HTTP auth*, dan *pause/resume* yang tidak diimplementasikan di sini.

## Script Simple Python
- [simpledirb.py](../../script/Dirb/index.md)

[Previously](00Whois.md) | [Next]()

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
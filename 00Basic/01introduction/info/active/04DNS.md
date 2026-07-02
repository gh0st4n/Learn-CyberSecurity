# DNS - Domain Name Server
## 1. Apa itu DNS?

**DNS (Domain Name System)** adalah sistem yang menerjemahkan nama domain yang mudah diingat manusia (seperti `google.com`) ke alamat IP numerik (seperti `142.250.64.78`) yang digunakan komputer untuk berkomunikasi.

### Perumpamaan Buku Telepon

Bayangkan DNS seperti **buku telepon raksasa** di internet:

- **Nama domain** = Nama orang yang ingin kamu hubungi (misal: "Budi")
- **Alamat IP** = Nomor telepon orang tersebut (misal: `021-555-1234`)
- **DNS Resolver** = Kamu yang membuka buku telepon dan mencari nama "Budi"
- **DNS Server** = Buku telepon itu sendiri - tempat penyimpanan semua data

Tanpa DNS, kita harus menghafal deretan angka IP untuk setiap website yang ingin dikunjungi. Sama seperti tanpa buku telepon, kamu harus hafal nomor telepon semua temanmu.

Prosesnya:

1. Kamu (browser) bilang: "Aku mau ke google.com"
2. DNS resolver cek: "Google.com itu IP-nya berapa ya?"
3. DNS server jawab: "142.250.64.78"
4. Browser langsung terhubung ke IP itu

## 2. DNS Zone Transfer

**DNS Zone Transfer** adalah mekanisme replikasi data DNS antar server. Server DNS utama (primary/ master) mengirimkan **seluruh isi database DNS**-nya ke server cadangan (secondary/ slave).

### Kenapa Ada Zone Transfer?

Supaya kalau server utama mati, server cadangan masih punya salinan lengkap data DNS dan bisa melayani permintaan. Ini dilakukan secara berkala atau saat ada perubahan data.

### Masalah Keamanan

Zone transfer menggunakan protokol **AXFR (Asynchronous Full Transfer Zone)**. Masalahnya: kalau server DNS dikonfigurasi salah (tidak membatasi siapa yang boleh minta transfer), **siapa pun bisa meminta salinan lengkap seluruh data DNS domain tersebut**.

Inilah yang membuatnya jadi target emas di fase information gathering.

### Perumpamaan

Bayangkan lagi buku telepon. Zone transfer yang tidak diamankan itu seperti:
- Buku telepon perusahaan diletakkan di lobi, terbuka, dan siapa pun boleh **memfotokopi seluruh isinya** - nama, jabatan, nomor telepon, alamat rumah semua karyawan.

Bandingkan dengan normalnya yang hanya seperti melihat satu halaman entri tertentu (query biasa).

## 3. Apa Guna Perintah `host -t ns` dan `host -t axfr`?

Kita bedah satu per satu:

### `$ host -t ns zoneserver.me`

Perintah ini melakukan **NS lookup** mencari nameserver (NS record) dari domain `zoneserver.me`.

```bash
$ host -t ns zoneserver.me
zoneserver.me name server nsztm1.digi.ninja.
zoneserver.me name server nsztm2.digi.ninja.
```

**Artinya:** Domain `zoneserver.me` dikelola oleh dua nameserver: `nsztm1.digi.ninja` dan `nsztm2.digi.ninja`.

**Tujuan di information gathering:**
- Mengetahui siapa pengelola DNS target
- Informasi ini diperlukan untuk langkah selanjutnya: mencoba zone transfer

### `$ host -t axfr zoneserver.me nsztm2.digi.ninja`

Perintah ini melakukan **AXFR zone transfer** meminta seluruh data DNS dari nameserver `nsztm2.digi.ninja` untuk domain `zoneserver.me`.

```bash
$ host -t axfr zoneserver.me nsztm2.digi.ninja
Trying "zoneserver.me"
Using domain server:
Name: nsztm2.digi.ninja
Address: 162.159.27.173#53
Aliases:

; Transfer failed.
```

Atau kalau **berhasil** (tidak diamankan), output-nya akan seperti:

```bash
zoneserver.me.        3600    IN      SOA     nsztm1.digi.ninja. hostmaster.zoneserver.me. 2024062801 7200 3600 1209600 3600
zoneserver.me.        3600    IN      NS      nsztm1.digi.ninja.
zoneserver.me.        3600    IN      NS      nsztm2.digi.ninja.
zoneserver.me.        3600    IN      A       162.159.27.173
www.zoneserver.me.    3600    IN      A       162.159.27.173
mail.zoneserver.me.   3600    IN      MX      10 mail.zoneserver.me.
admin.zoneserver.me.  3600    IN      TXT     "Contact: admin@zoneserver.me"
vpn.zoneserver.me.    3600    IN      A       10.10.10.5
```

**Tujuan di information gathering:**
- Mendapatkan **semua subdomain** yang terdaftar
- Menemukan server internal (IP private seperti `10.10.10.5` di atas) yang seharusnya tidak terekspos publik
- Melihat record MX (mail server), TXT (catatan teks), dan lainnya
- Memetakan seluruh infrastruktur digital target dari satu celah miskonfigurasi

## 4. Mengapa DNS Penting untuk Information Gathering?

DNS adalah **sumber informasi paling awal dan paling kaya** dalam proses penetration testing. Berikut alasannya:

| Aspek | Penjelasan                                                                                                                 |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| **Footprinting** | DNS mengungkap struktur organisasi target subdomain memberi petunjuk fungsi tiap server (mail, vpn, api, dev, admin, dsb.) |
| **Low Noise** | Query DNS terlihat seperti lalu lintas normal dan tidak menimbulkan alarm IDS/IPS                                          |
| **Subdomain Enumeration** | Menemukan subdomain yang tidak terindeks Google = attack surface tersembunyi                                               |
| **IP Range Mapping** | Dari A record, kamu bisa tahu blok IP yang digunakan target                                                                |
| **Miskonfigurasi** | Zone transfer yang terbuka adalah holy grail semua data langsung didapat tanpa brute force                                 |
| **TXT Record** | Sering berisi informasi sensitif: token verifikasi, kunci API, konfigurasi SPF/DKIM                                        |

**Ringkasnya:** DNS adalah peta jalan target. Semakin banyak data DNS yang terkumpul, semakin besar surface area untuk eksploitasi.

## 5. Arti Tipe-Tipe DNS Record

Berikut penjelasan masing-masing tipe record yang kamu tanyakan:

### **A (Address Record)**
- **Fungsi:** Memetakan nama domain ke **alamat IPv4**
- **Contoh:** `google.com A 142.250.64.78`
- **Guna di Pentest:** Mengetahui IP publik target, bisa langsung di-scan port-nya

### **AAAA (IPv6 Address Record)**
- **Fungsi:** Memetakan nama domain ke **alamat IPv6**
- **Contoh:** `google.com AAAA 2a00:1450:4009:81d::200e`
- **Guna di Pentest:** Server kadang hanya diamankan di IPv4, tapi IPv6-nya terbuka potensi bypass firewall

### **MX (Mail Exchange Record)**
- **Fungsi:** Menentukan server email yang menangani email untuk domain tersebut. Ada prioritas (angka lebih kecil = prioritas lebih tinggi)
- **Contoh:** `example.com MX 10 mail.example.com`
- **Guna di Pentest:** Mengetahui alamat mail server target bisa untuk phishing, SPF/DKIM bypass, atau serangan langsung ke port SMTP

### **NS (Nameserver Record)**
- **Fungsi:** Menentukan server DNS yang berwenang (authoritative) untuk suatu domain
- **Contoh:** `example.com NS ns1.example.com`
- **Guna di Pentest:** Langkah awal untuk zone transfer. Juga bisa untuk DNS poisoning atau subdomain takeover kalau NS-nya sudah tidak terdaftar

### **TXT (Text Record)**
- **Fungsi:** Menyimpan data teks arbitrer. Sering dipakai untuk verifikasi kepemilikan domain, SPF, DKIM, DMARC
- **Contoh:**
  ```
  example.com TXT "v=spf1 include:_spf.google.com ~all"
  example.com TXT "google-site-verification=xyz123"
  ```
- **Guna di Pentest:** Sumber informasi emas kadang berisi kunci API, token, kredensial yang bocor. Juga untuk mengkonfigurasi serangan email spoofing (cek SPF)

### **AFSDB (Andrew File System Database)**
- **Fungsi:** Menunjuk ke server AFS (Distributed File System dari Carnegie Mellon University). Digunakan di lingkungan universitas/korporasi tertentu
- **Contoh:** `example.com AFSDB 1 afsdb.example.com`
- **Guna di Pentest:** Jarang ditemui, tapi kalau ada indikasi infrastruktur lawas dengan protokol yang mungkin tidak dipatch

### **LOC (Location Record)**
- **Fungsi:** Menyimpan **koordinat geografis** (lintang, bujur, ketinggian) dari suatu server/domain
- **Contoh:** `server.example.com LOC 51 30 12.748 N 0 7 39.612 W 0m 0m 0m 0m`
- **Guna di Pentest:** Informasi OSINT bisa mengungkap lokasi fisik data center target. Berguna untuk social engineering atau serangan fisik di red team engagement

### **NAPTR (Naming Authority Pointer)**
- **Fungsi:** Digunakan dalam telekomunikasi dan VoIP membantu penerjemahan nomor telepon ke URI (SIP, email, dll) melalui aturan regex/rewrite
- **Contoh:**
  ```
  example.com NAPTR 100 10 "u" "E2U+sip" "!^.*$!sip:customer@example.com!" .
  ```
- **Guna di Pentest:** Jika target punya infrastruktur VoIP/SIP bisa untuk enumerasi ekstensi, discovery server SIP, atau serangan VoIP fraud

# Tools
## 1. Tools Baris Perintah Dasar (Bawaan Sistem)

### **`dig`** - DNS Swiss Army Knife
Ini tool DNS paling powerfull. Lebih detail daripada `host`.

```bash
# NS lookup (cari nameserver)
dig zoneserver.me NS

# Zone transfer (AXFR) langsung ke nameserver spesifik
dig @nsztm2.digi.ninja zoneserver.me AXFR

# A record
dig google.com A

# AAAA record
dig google.com AAAA

# MX record
dig google.com MX

# TXT record
dig google.com TXT

# ANY record (semua tipe - tapi banyak DNS server sekarang ignore ANY)
dig google.com ANY

# Short output (hanya jawaban)
dig google.com A +short

# Trace resolusi DNS dari root
dig google.com A +trace
```

**Keunggulan `dig` dibanding `host`:**
- Output lebih terstruktur dan detail
- Bisa trace resolusi dari root nameserver
- Header flags (AA, RD, RA) terlihat - berguna untuk debug

### **`nslookup`** - Legacy Tool (masih berguna)

```bash
# Mode interaktif
nslookup
> server nsztm2.digi.ninja      # ganti nameserver
> set type=any                   # set tipe record
> zoneserver.me                  # query domain
> ls -d zoneserver.me            # coba zone transfer (setara AXFR)
> exit

# Mode non-interaktif
nslookup -type=ns zoneserver.me
nslookup -type=axfr zoneserver.me nsztm2.digi.ninja
```

## 2. Tools Information Gathering Khusus (Yang Paling Sering Dipakai)

### **`dnsrecon`** - DNS Enumeration Profesional

```bash
# Install
sudo apt install dnsrecon -y

# Basic enumeration - A, AAAA, MX, NS, SOA, TXT
dnsrecon -d zoneserver.me

# Zone transfer attempt
dnsrecon -d zoneserver.me -t axfr

# Brute force subdomain dengan wordlist
dnsrecon -d zoneserver.me -D /usr/share/wordlists/subdomains.txt -t brt

# Enumerate SRV records (service discovery sangat berguna)
dnsrecon -d zoneserver.me -t srv

# Reverse lookup dari range IP
dnsrecon -r 162.159.27.0/24 -t rvl
```

**Kenapa `dnsrecon` lebih enak?** Dia otomatis cari semua tipe record, coba zone transfer, bahkan bisa reverse lookup range IP dalam satu perintah.

### **`dnsenum`** - Enumeration Multi-Langkah

```bash
# Install
sudo apt install dnsenum -y

# Full enumeration - NS, MX, AXFR, brute force subdomain, Google scraping
dnsenum zoneserver.me

# Dengan wordlist kustom
dnsenum -f /usr/share/wordlists/subdomains.txt zoneserver.me

# Threading lebih cepat
dnsenum --threads 10 zoneserver.me
```

`dnsenum` otomatis melakukan:
1. NS lookup
2. MX lookup
3. Zone transfer attempt
4. Subdomain brute force
5. Google scraping untuk subdomain
6. Reverse lookup IP

### **`fierce`** - DNS Bruteforce & Range Discovery

```bash
# Install
sudo apt install fierce -y

# Basic scan
fierce --domain zoneserver.me

# Dengan wordlist dan nameserver spesifik
fierce --domain zoneserver.me --wordlist /usr/share/wordlists/subdomains.txt --dns-servers 8.8.8.8
```

Fierce terkenal untuk menemukan subdomain yang "tersembunyi" dan bisa otomatis melakukan zone discovery (menebak range IP).

## 3. Tools Berbasis Web & OSINT

### **`theHarvester`** - OSINT Multisource

```bash
# Install
sudo apt install theharvester -y

# Kumpulkan dari DNS, Google, Bing, LinkedIn, dll
theharvester -d zoneserver.me -b google,bing,dns

# DNS brute force
theharvester -d zoneserver.me -b dns -l 500
```

### **`amass`** - The Heavyweight (OWASP Project)

```bash
# Install
sudo apt install amass -y

# Enumeration dengan berbagai sumber (DNS, cert transparancy, reverse DNS, dll)
amass enum -d zoneserver.me

# Passive mode (tidak menyentuh target langsung)
amass enum -passive -d zoneserver.me

# Dengan API key untuk hasil lebih lengkap
amass enum -d zoneserver.me -config config.ini
```

`amass` menggabungkan:
- DNS brute force
- Certificate Transparency logs (crt.sh)
- Reverse DNS
- Scraping search engine
- API pihak ketiga (Shodan, VirusTotal, dll)
- RIPE WHOIS

## 4. Perbandingan Cepat Tools

| Tool | Kelebihan | Kekurangan |
|---|---|---|
| `dig` | Clean output, +trace, +short | Manual per query |
| `host` | Simpel, output minimal | Terlalu sederhana |
| `dnsrecon` | Lengkap, auto multi-record | Output kadang verbose |
| `dnsenum` | Multi-sumber (google scraping) | Agak lambat |
| `fierce` | Bagus untuk range discovery | Tak semodern amass |
| `amass` | Paling komprehensif | Berat, perlu API key optimal |
| `theHarvester` | OSINT + email scraping | Fokusnya bukan murni DNS |

## 5. Tips Information Gathering DNS

**Urutan kerja yang efektif:**

```bash
# 1. Cari nameserver dan basic info
dig target.com NS +short
dig target.com MX +short
dig target.com TXT +short

# 2. Coba zone transfer ke semua nameserver yang ditemukan
for ns in $(dig target.com NS +short); do
    echo "[*] Trying $ns"
    dig @$ns target.com AXFR
done

# 3. Brute force subdomain dengan wordlist
dnsrecon -d target.com -D /usr/share/wordlists/subdomains.txt -t brt

# 4. Certificate Transparency (sering nemu subdomain baru)
curl -s "https://crt.sh/?q=%25.target.com&output=json" | jq -r '.[].name_value' | sort -u

# 5. Amass untuk hasil maksimal
amass enum -d target.com -o output.txt
```

**Wordlist yang berguna:**
- `/usr/share/wordlists/dirb/common.txt`
- `/usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt`
- `/usr/share/wordlists/amass/subdomains.lst`

## Script Python
- [Script Python](../../script/DNS/index.md)


[Previously](03Dirhunt.md) | [Next](05Nmap.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
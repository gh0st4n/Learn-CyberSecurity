# Mengenal Whois: Protokol, Teknik, Instalasi, dan Implementasinya

## Apa Itu Whois?

**Whois** adalah protokol query/response berbasis TCP (port 43) yang digunakan untuk menanyakan database yang menyimpan informasi registrasi sumber daya internet seperti domain, blok IP, dan ASN (Autonomous System Numbers). Database ini dikelola oleh **RIR (Regional Internet Registry)** dan **domain registrar**.

Informasi yang biasa didapat dari query whois meliputi:
- Nama pemilik domain/alamat IP
- Tanggal pendaftaran, pembaruan, dan kadaluwarsa
- Name server (NS) yang digunakan
- Kontak administratif, teknis, dan billing
- Status domain (active, pending delete, clientHold, dll.)

## Teknik yang Digunakan dalam Whois

Teknik whois dalam konteks cybersecurity umumnya digunakan pada fase **reconnaissance** (OSINT). Berikut beberapa teknik lanjutan yang biasa dipraktikkan:

### 1. **Direct Query ke Port 43**
Daripada menggunakan tool seperti `whois`, kita bisa melakukan query langsung via koneksi raw TCP ke server whois tertentu.

```bash
echo "example.com" | nc -w 5 whois.verisign-grs.com 43
```

### 2. **Thick vs Thin Whois**
- **Thin Whois** - hanya memberikan informasi registrar dan name server. Data pemilik harus di-query ke registrar masing-masing.
- **Thick Whois** - memberikan data lengkap termasuk informasi pemilik langsung dari satu server.

Tool whois modern otomatis melakukan follow-up dari thin ke thick server.

### 3. **Whois History (Reverse Whois)**
Mencari riwayat kepemilikan domain melalui third-party seperti WhoisXML, DomainTools, atau SecurityTrails. Ini berguna untuk menemukan infrastruktur lain milik target yang sama.

### 4. **IP Whois & ASN Enumeration**
Mencari tahu netblock dan ASN yang dimiliki organisasi target untuk memperluas permukaan serangan.

### 5. **Domain Brute-force via Whois**
Mendaftarkan domain yang mirip (typosquatting) lalu memonitor whois-nya untuk mendeteksi takeover atau infeksi.

## Cara Install & Menggunakan Whois

### Instalasi di Linux (Kali/Debian/Ubuntu)

```bash
sudo apt update && sudo apt install whois -y
```

### Instalasi di macOS

```bash
brew install whois
```

### Instalasi di Windows

Download dari situs Microsoft Sysinternals atau gunakan WSL. Alternatif: gunakan Python (lihat script di bawah).

### Penggunaan Dasar

```bash
# Query informasi domain
whois example.com

# Query informasi IP
whois 8.8.8.8

# Ganti server whois secara manual
whois -h whois.verisign-grs.com example.com

# Gunakan port non-default
whois -p 4343 example.com

# Simpan hasil ke file
whois example.com > whois_output.txt
```

### Contoh Output

```
$ whois google.com

Domain Name: GOOGLE.COM
Registry Domain ID: 2138514_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.markmonitor.com
Registrar URL: http://www.markmonitor.com
Updated Date: 2019-09-09T15:39:04Z
Creation Date: 1997-09-15T04:00:00Z
Registry Expiry Date: 2028-09-14T04:00:00Z
Registrar: MarkMonitor Inc.
Registrar IANA ID: 292
Registrar Abuse Contact Email: abusecomplaints@markmonitor.com
Registrar Abuse Contact Phone: +1.2083895740
Domain Status: clientDeleteProhibited
Domain Status: clientTransferProhibited
Domain Status: clientUpdateProhibited
Name Server: NS1.GOOGLE.COM
Name Server: NS2.GOOGLE.COM
Name Server: NS3.GOOGLE.COM
Name Server: NS4.GOOGLE.COM
DNSSEC: unsigned
URL of the ICANN Whois Inaccuracy Complaint Form: https://www.icann.org/wicf/
```

## Alur Kerja Whois

Berikut diagram alur kerja whois secara umum:

```
┌─────────────┐      Query via Port 43        ┌─────────────────┐
│   Client    │ ────────────────────────────→ │  Whois Server   │
│ (whois CLI) │                               │ (Registrar/RIR) │
│  / Script   │ ←──────────────────────────── │  port 43/TCP    │
└─────────────┘       Raw Text Response       └─────────────────┘
       │                                               │
       │                                               ▼
       │                                        ┌──────────────┐
       │                                        │    RDAP      │
       │                                        │  (modern,    │
       │                                        │  JSON-based) │
       │                                        └──────────────┘
       ▼
┌─────────────────┐
│  Parsing Output │
│  - Ekstrak NS   │
│  - Tanggal      │
│  - Registrar    │
│  - Kontak       │
└─────────────────┘
```

**Alur detailnya:**

1. **User** menjalankan perintah `whois domain.tld`
2. **Client whois** menentukan server whois yang sesuai (berdasarkan TLD atau IP range)
3. **Koneksi TCP** dibuat ke port 43 server whois
4. **Query string** dikirim (nama domain/IP) diikuti `\r\n`
5. **Server** merespon dengan teks mentah berisi data registrasi
6. **Koneksi ditutup** oleh server
7. **Output** ditampilkan ke pengguna

> **Catatan:** Saat ini **RDAP (Registration Data Access Protocol)** mulai menggantikan whois. RDAP menggunakan HTTP/HTTPS dan mengembalikan data dalam format JSON/XML terstruktur. Namun whois masih dominan digunakan karena kesederhanaannya.

## Penggunaan dalam Cybersecurity

Dalam konteks penetration testing, whois digunakan pada fase **Reconnaissance / OSINT** untuk:

1. **Mengidentifikasi infrastruktur target** - blok IP, ASN, netblock memungkinkan kita menemukan seluruh surface target
2. **Social Engineering** - informasi kontak (email, telepon) bisa digunakan untuk phishing atau pretexting
3. **Domain Discovery** - temukan domain lain yang dimiliki oleh organisasi yang sama dengan mencocokkan email atau nama registrant
4. **Deteksi typosquatting** - cek domain yang mirip dengan domain target untuk campaign phising atau brand impersonation
5. **Privasi registrant** - analisis apakah target menggunakan WHOIS privacy protection atau tidak; jika tidak, datanya bisa langsung dikumpulkan

## Script Python
[Script Python](script/whois/index.md)

[Previously](../pasive/02Netcraft.md) | [Next](01Dirb.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
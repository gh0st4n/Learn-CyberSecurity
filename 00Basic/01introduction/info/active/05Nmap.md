# Nmap
## Apa Itu Nmap?

**Nmap** (Network Mapper) adalah tools keamanan jaringan open-source yang digunakan untuk **menemukan host, memindai port, mendeteksi service/versi, fingerprinting OS**, dan berbagai teknik discovery lainnya. Dikembangkan oleh Gordon Lyon (Fyodor) dan dirilis pertama tahun 1997, nmap menjadi standar de facto dalam reconnaissance fase penetration testing.

## Teknik-Teknik Scan Nmap

Nmap menggunakan beberapa teknik utama:

### 1. TCP Connect Scan (`-sT`)
Melakukan three-way handshake penuh. Paling mudah terdeteksi.

### 2. SYN Scan / Half-Open Scan (`-sS`)
Mengirim SYN, jika SYN/ACK balas → port terbuka, lalu RST. Tidak menyelesaikan handshake. Lebih cepat & stealthy. **Default scan nmap**.

### 3. UDP Scan (`-sU`)
Mengirim paket UDP kosong. Respon ICMP Port Unreachable → tertutup. Tidak ada respon → terbuka/filtered. Sangat lambat.

### 4. Version Detection (`-sV`)
Setelah menemukan port terbuka, nmap mengirim probe untuk menentukan service name & version.

### 5. OS Detection (`-O`)
Mengidentifikasi sistem operasi target berdasarkan fingerprint respon TCP/IP (TTL, window size, TCP options).

### 6. Aggressive Mode (`-A`)
Menggabungkan: OS detection (`-O`), version detection (`-sV`), script scanning (`-sC`), dan traceroute. **Paling berisik dan berat.**

### 7. Timing Templates (`-T0` sampai `-T5`)
- **T0 / Paranoid**: Serialisasi, 5 menit delay antar probe, anti-IDS
- **T1 / Sneaky**: 15 detik delay, masih slow
- **T2 / Polite**: 0.4 detik delay . sopan, kurangi bandwidth
- **T3 / Normal**: Default, tanpa delay tambahan
- **T4 / Aggressive**: Timeout 1.25x RTT, probing lebih agresif
- **T5 / Insane**: Timeout 0.3x RTT, parallelism tinggi, **sangat cepat, sangat berisik**

# Analisis Command yang Anda Berikan

### 1. `nmap -sV -T5` - Kenapa "Dilarang"?

```bash
nmap -sV -T5
```

| Komponen | Fungsi                                                                                           |
| -------- | ------------------------------------------------------------------------------------------------ |
| `-sV`    | Version detection - mengirim probe ke port terbuka untuk identifikasi service                    |
| `-T5`    | Timing insane - **mengirim paket secepat mungkin, timeout sangat singkat, parallelism maksimum** |

**Kenapa dikatakan "dilarang karena sistem gak kuat"?**

- `-T5` mengirim **ratusan hingga ribuan paket per detik** secara paralel
- Version detection (`-sV`) memperparah karena setelah port ditemukan, nmap mengirim probe tambahan untuk fingerprinting service
- Kombinasi ini bisa menyebabkan:
  - **Crash pada perangkat embedded** (router, switch IoT) yang CPU/memory-nya terbatas
  - **Load tinggi pada server** yang tidak punya rate limiting
  - **False negatives**: karena timeout sangat singkat (`--host-timeout` default lebih kecil), service lambat tidak terdeteksi
  - **IDS/IPS langsung trigger alarm** - sangat berisik

Singkatnya: `-T5` itu seperti **hammer drill** ke port target. Efektif di lab, berbahaya di production.

### 2. `nmap -sV -T5 -p 21 -A`

```bash
nmap -sV -T5 -p 21 -A
```

- `-p 21` → scan port FTP saja
- `-A` → Aggressive: OS detection + version detection + script scan + traceroute

**Analisis**: 
- FTP port 21 biasanya di sistem stabil, tapi kombinasi `-T5 -A` masih tetap **agresif**
- `-A` menjalankan script NSE seperti `ftp-anon.nse`, `ftp-bounce.nse`, dll
- Risiko: FTP server versi lama bisa crash dengan banyak probe paralel

### 3. `nmap -sV -T5 -p 80 -A`

- HTTP port 80 - umumnya lebih stabil
- Script yang berjalan: `http-title`, `http-server-header`, `http-methods`, dll.
- Potensi crash lebih rendah, tapi tetap **high noise**

### 4. `nmap -sV -T5 -p 139 -A`

- Port 139 = NetBIOS Session Service (SMB over NetBIOS)
- `-A` akan menjalankan script SMB seperti `smb-os-discovery`, `smb-security-mode`, dll.
- **SMB sangat sensitif** - Windows versi lama (XP/2003) bisa **BSOD** dengan probe SMB agresif
- Sistem non-Windows (Samba) bisa hang

### 5. `nmap -sV -T5 -p 8022 -A`

- Port non-standar. Biasanya SSH atau custom service
- `-A` akan mencoba fingerprinting SSH + script NSE seperti `ssh-hostkey`, `ssh-auth-methods`
- Risiko lebih rendah, tapi jika ternyata service custom, probe agresif bisa menyebabkan crash

## Cara Install Nmap

### Kali Linux (pre-installed)
```bash
sudo apt update && sudo apt install nmap -y
```

### Ubuntu/Debian
```bash
sudo apt update && sudo apt install nmap -y
```

### macOS
```bash
brew install nmap
```

### Windows
Download installer dari https://nmap.org/download.html

### Verifikasi install
```bash
nmap --version
```

## Cara Menggunakan Nmap (Dasar)

### Scan satu target
```bash
nmap <target_IP>
```

### Scan range port spesifik
```bash
nmap -p 80,443,8080 192.168.1.1
nmap -p 1-1000 192.168.1.1
```

### Version detection
```bash
nmap -sV 192.168.1.1
```

### OS detection
```bash
nmap -O 192.168.1.1
```

### Aggressive scan (hati-hati!)
```bash
nmap -A 192.168.1.1
```

### Timing template aman untuk production
```bash
nmap -T3 -sV 192.168.1.1   # normal, stabil
nmap -T4 -sV 192.168.1.1   # agresif, masih OK untuk web server
```

### Save output
```bash
nmap -oN hasil.txt 192.168.1.1   # normal output
nmap -oX hasil.xml 192.168.1.1   # XML
nmap -oG hasil.grep 192.168.1.1  # greppable
```

## Alur Kerja (Workflow) Nmap

```
                        +-------------------+
                        |    INPUT TARGET   |
                        | (IP/domain/range) |
                        +--------+----------+
                                 |
                                 v
                        +--------------------+
                        |  HOST DISCOVERY    |  <-- Ping scan (-sn)
                        |  (Apakah host up?) |
                        +--------+-----------+
                                 |
                         [Host hidup?]
                              / \
                            Ya   Tidak → Stop
                             |
                             v
                        +---------------------+
                        |  PORT SCANNING      |  <-- SYN/TCP/UDP/SCTP
                        |  (Port apa terbuka?)|
                        +--------+------------+
                                 |
                                 v
                        +---------------------+
                        | SERVICE DETECTION   |  <-- -sV
                        |  (Banner grabbing,  |
                        |   probe fingerprint)|
                        +--------+------------+
                                 |
                                 v
                        +-------------------+
                        |  OS DETECTION     |  <-- -O
                        |  (TCP/IP stack    |
                        |   fingerprinting) |
                        +--------+----------+
                                 |
                                 v
                        +--------------------+
                        |  SCRIPT SCANNING   |  <-- -sC atau --script
                        |  (NSE: vuln check, |
                        |   brute, exploit)  |
                        +--------+-----------+
                                 |
                                 v
                        +--------------------+
                        |   TRACEROUTE       |  <-- (bagian -A)
                        |   (Hop discovery)  |
                        +--------+-----------+
                                 |
                                 v
                        +--------------------+
                        |     OUTPUT         |
                        | (normal/XML/grep)  |
                        +--------------------+
```

### Tahapan Detail:

1. **Host Discovery**: Nmap mengirim ICMP echo, TCP SYN ke port 443/80, TCP ACK, ICMP timestamp. Host dianggap hidup jika ada satu respon.

2. **Port Scanning**: Untuk setiap host hidup, nmap mengirim probe ke port yang ditentukan. Menganalisis respon SYN/ACK (open), RST (closed), atau tidak ada (filtered).

3. **Service Detection** (`-sV`): Port terbuka → probe khusus dikirim untuk memicu banner. Database signature nmap-service-probes mencocokkan respon → service name + version.

4. **OS Detection** (`-O`): Mengirim serangkaian paket TCP/UDP khusus (SEQ, OPS, WIN, T1-T7, IE, EC, etc). Mencocokkan fingerprint di nmap-os-db.

5. **Script Scanning** (NSE): Menjalankan script Lua. Kategori: auth, default, discovery, dos, exploit, intrusive, malware, safe, vuln, etc.

6. **Traceroute**: Mengirim paket dengan TTL incremental untuk mapping hop.

7. **Output**: Semua data dikompilasi dan ditampilkan sesuai format.

## Rekomendasi untuk Penggunaan Aman

| Jangan lakukan                        | Alternatif                                  |
| ------------------------------------- | ------------------------------------------- |
| `-T5` di production                   | `-T3` atau `-T4`                            |
| `-A` tanpa perlindungan               | `-sV -sC` terpisah                          |
| Scan paralel banyak host dengan `-T5` | Scan bertahap, 1-5 host saja                |
| Version detection di semua port       | Scan port penting dulu, baru `-sV` di hasil |

**Bottom line**: `nmap -sV -T5 -A` adalah **sledgehammer**. Efektif untuk lab CTF/HTB, tapi di jaringan production kamu bisa menyebabkan **denial of service** pada perangkat yang rapuh. Gunakan `-T3` atau `-T4` sebagai batas aman untuk penetration testing profesional.

[Previously](04DNS.md) | [Next](06wpscan.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
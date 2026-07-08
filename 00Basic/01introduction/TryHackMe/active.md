# Active Reconnaissance

**Active Reconnaissance** adalah proses berinteraksi langsung dengan sistem atau jaringan target untuk mengumpulkan informasi tentangnya. Pengintaian pasif mengumpulkan data dari sumber publik tanpa mengirimkan lalu lintas apa pun ke target. Sebaliknya, pengintaian aktif memerlukan pengiriman paket, pembuatan koneksi, dan pengujian layanan. Perbedaan ini penting karena teknik aktif meninggalkan jejak berupa entri log. peringatan, blokir WAF, dan pemicu.

## Catatan Pengintaian Aktif Menggunakan Peramban Web (Web Browser)

Peramban web adalah salah satu alat yang paling mudah digunakan dan paling tidak mencurigakan untuk **pengintaian aktif (active reconnaissance)**. Karena terdapat di hampir setiap sistem, lalu lintasnya menyatu dengan aktivitas pengguna normal, sehingga menyulitkan tim bertahan (Blue Team) untuk membedakan antara pengintaian dan penjelajahan sah.

### 1. Dasar-Dasar Tingkat Transportasi (Transport Layer)

- **Port 80 (HTTP):** Digunakan secara _default_ untuk lalu lintas data teks biasa (_plain text_). Saat ini sudah jarang digunakan karena sebagian besar situs otomatis mengalihkan (redirect) ke HTTPS.
    
- **Port 443 (HTTPS):** Standar industri saat ini untuk koneksi web yang aman dan terenkripsi.
    
- **HTTP/3 & Protokol QUIC:** * Banyak situs modern mendukung **HTTP/3** yang berjalan di atas protokol **QUIC** (dikembangkan oleh Google).
    
    - QUIC menggabungkan fungsi dari **TCP** (keandalan) dan **TLS** (keamanan/enkripsi) ke dalam satu protokol yang berjalan di atas **UDP** pada port 443.
        
    - **Identifikasi:** Anda dapat melihat lalu lintas HTTP/3 di tab _Network_ pada Developer Tools, di mana kolom protokol akan menampilkan label `h3`.
        
- **Port Non-Standar:** Anda dapat mengakses layanan pada port kustom dengan menentukannya langsung di URL.
    
    - _Contoh:_ `https://target.com:8443/` atau `http://192.168.1.100:8080/`
        

### 2. Alat Pengembang (Developer Tools / DevTools)

Untuk membuka DevTools, gunakan pintasan keyboard berikut:

- **Windows/Linux:** `Ctrl + Shift + I`
    
- **macOS:** `Option + Command + I`
    

Berikut adalah tab-tab krusial yang digunakan untuk pengintaian:

- ### Tab Network (Jaringan)
    
    Menampilkan semua permintaan (_requests_) dan respons (_responses_) secara real-time.
    
    - **Informasi penting:** Header respons seperti `Server`, `X-Powered-By`, dan `Content-Security-Policy`.
        
    - **Data lain:** Informasi waktu (_timing_), kode status HTTP (200, 403, 404, dll), serta cookie yang dikirim/diterima.
        
- ### Tab Console (Konsol)
    
    Memungkinkan Anda mengeksekusi kode JavaScript langsung dalam konteks halaman, melihat error, dan berinteraksi dengan DOM (_Document Object Model_).
    
- ### Tab Sources / Debugger (Sumber)
    
    Tempat untuk menelusuri file JavaScript, CSS, dan HTML yang dimuat. Ini adalah salah satu teknik pengintaian paling praktis.
    
    - **Temuan potensial:** File JavaScript sering kali mengandung kode yang dikodekan secara permanen (_hardcoded_), seperti _API endpoints_, struktur direktori, referensi ke layanan internal, dan komentar pengembang (_developer comments_) yang lupa dihapus.
        
- ### Tab Application / Storage (Aplikasi)
    
    Digunakan untuk memeriksa data yang disimpan di sisi klien: Cookie, _Local Storage_, dan _Session Storage_.
    
    - **Temuan potensial:** Token sesi (session tokens), kunci API (API keys) yang terekspos secara tidak sengaja, serta data pelacakan atau autentikasi.
        
- ### Tab Security (Keamanan)
    
    Menyediakan rincian sertifikat SSL/TLS, termasuk pihak penerbit, masa berlaku, dan **Subject Alternative Names (SAN)**. SAN sering kali mengungkap subdomain tambahan atau domain terkait milik organisasi target.
    

### 3. Ekstensi Peramban (Browser Extensions)

Ekstensi dapat mengubah browser standar menjadi platform pengintaian yang kuat:

- **FoxyProxy:** Mempermudah peralihan antar-proxy (seperti **Burp Suite** atau **OWASP ZAP**) dan terowongan SOCKS5 untuk mencegat (_intercept_) lalu lintas data.
    
- **User-Agent Switcher and Manager:** Mengubah string _User-Agent_ untuk memalsukan browser, OS, atau perangkat yang Anda gunakan (misalnya meniru Safari seluler untuk mencari endpoint khusus _mobile_).
    
    > **Catatan:** WAF dan CDN modern dapat mendeteksi perubahan User-Agent yang terlalu cepat atau mencurigakan.
    
- **Wappalyzer:** Secara pasif mengidentifikasi teknologi yang digunakan pada situs web, seperti CMS/Platform, server web, _framework_ JavaScript, alat analitik, CDN, dan basis data.
    

#### Alternatif Ekstensi Lainnya:

- **BuiltWith Technology Profiler:** Mirip dengan Wappalyzer, terkadang mendeteksi teknologi yang terlewat oleh ekstensi lain.
    
- **WhatRuns:** Alternatif pemindai teknologi yang lebih ringan.
    
- **Library Detector:** Khusus mendeteksi versi pustaka dan _framework_ JavaScript yang digunakan.
    

### 4. Mode Operasi & Siluman (Stealth)

Meskipun aktivitas penjelajahan lewat browser terlihat normal, pola yang tidak biasa tetap dapat memicu alarm pada **WAF (Web Application Firewall)** atau sistem deteksi ujung (_Endpoint Detection_).

Sinyal mencurigakan yang dipantau oleh tim bertahan meliputi:

1. Pemuatan halaman yang terlalu cepat (tidak manusiawi).
    
2. Header permintaan yang dimodifikasi secara tidak wajar.
    
3. Penggunaan DevTools yang konstan dan tidak biasa.
    
4. String _User-Agent_ yang tidak konsisten atau abnormal.
    

> **Tujuan Utama:** Selalu tiru perilaku pengguna yang sah (_legitimate user_) sebisa mungkin untuk menghindari deteksi.

## Ping

Nama `ping` diambil dari prinsip kerja **sonar** pada kapal selam. Konsepnya sederhana: Anda mengirimkan suatu sinyal gelombang ke arah target dan mendengarkan gema (_echo_) yang memantul kembali.

Di dalam jaringan komputer, perintah `ping` mengadopsi cara yang sama. Ini adalah alat pengintaian aktif paling mendasar yang digunakan untuk mendeteksi apakah sebuah host tujuan sedang aktif (_online_) dan dapat dijangkau di dalam jaringan sebelum kita melakukan pemindaian yang lebih mendalam.

## 1. Mekanisme Kerja dan Struktur Paket ICMP

Perintah `ping` bekerja menggunakan protokol **ICMP** (_Internet Control Message Protocol_). Proses ini melibatkan pertukaran dua jenis paket utama secara cepat:

1. **ICMP Echo Request (Type 8):** Paket uji yang dikirimkan oleh komputer Anda ke alamat target.
    
2. **ICMP Echo Reply (Type 0):** Paket balasan yang dikirimkan oleh target kembali ke komputer Anda, menandakan bahwa ia menerima pesan tersebut dengan baik.
    

### Anatomi Ukuran Paket dan Header ICMP

Ketika Anda melakukan ping, data yang dikirimkan dibungkus dalam beberapa lapisan. Di sinilah pentingnya memahami struktur ukuran paket:

- **Header ICMP berukuran tepat 8 byte.** Header ini wajib ada pada setiap paket ICMP karena berfungsi sebagai "surat pengantar" yang berisi informasi kritis seperti _Type_ (jenis pesan), _Code_ (sub-informasi), _Checksum_ (validasi anti-korup data), serta _Sequence Number_ untuk mengurutkan paket.
    
- **Ukuran Data Bawaan (Default Payload):** Secara standar pada sistem operasi Linux, data murni (_payload_) yang disisipkan di dalam paket _Echo Request_ adalah sebesar **56 byte**.
    
- **Total Ukuran Paket:** Jika Anda melihat baris perintah `PING MACHINE_IP (MACHINE_IP) 56(84) bytes of data`, angka **84** berasal dari penjumlahan data murni (56 byte) + Header ICMP (8 byte) + Header IP versi 4 (20 byte).
    

### Mengubah Ukuran Data dengan Opsi `-s`

Dalam kondisi tertentu—seperti menguji batas maksimum transmisi jaringan (_Maximum Transmission Unit_ / MTU) atau mensimulasikan beban jaringan—kita perlu mengubah ukuran data tersebut.

Anda bisa menggunakan **opsi `-s`** (_Size_) diikuti dengan jumlah bita yang diinginkan.

Bash

```
# Mengirim paket ping dengan muatan data kustom sebesar 1000 byte
ping -s 1000 MACHINE_IP
```

## 2. Cara Penggunaan di Berbagai Sistem Operasi

Secara bawaan, cara kerja ping di beberapa OS memiliki sedikit perbedaan pada kontrol jumlah paket yang dikirimkan.

### Pengaturan Jumlah Paket (Count)

- **Linux & macOS:** Menggunakan flag **`-c`**. Jika Anda tidak menentukan jumlahnya, ping akan berjalan terus-menerus tanpa henti hingga Anda menekan tombol `Ctrl + C`.
    
    Bash
    
    ```
    ping -c 5 tryhackme.com
    ```
    
- **Windows:** Menggunakan flag **`-n`**. Secara default, Windows hanya akan mengirimkan 4 paket lalu berhenti otomatis.
    
    DOS
    
    ```
    ping -n 5 MACHINE_IP
    ```
    

### Memaksa Protokol IP versi 4 atau 6

Jika sebuah domain mendukung teknologi _dual-stack_ (memiliki IPv4 dan IPv6 sekaligus), Anda bisa memaksa peramban jaringan menggunakan versi spesifik dengan flag `-4` atau `-6`:

Bash

```
ping -4 -c 5 target.com      # Memaksa koneksi lewat IPv4
ping -6 -c 5 target.com      # Memaksa koneksi lewat IPv6
```

## 3. Membaca dan Menginterpretasikan Hasil Output

### Kasus Sukses: Target Merespons (Alive)

Plaintext

```
64 bytes from MACHINE_IP: icmp_seq=1 ttl=64 time=0.512 ms
```

- **0% Packet Loss:** Menandakan jalur koneksi antara Anda dan target sangat bersih tanpa gangguan.
    
- **Waktu Respons (RTT / Round-Trip Time):** Waktu putar balik paket (misal: `0.512 ms`). Semakin kecil angkanya, semakin dekat jarak fisik atau logis target.
    

> ### 💡 Teknik OS Fingerprinting Melalui TTL (Time To Live)
> 
> **TTL** bukanlah penunjuk durasi waktu, melainkan **batas maksimum jumlah router (_hops_)** yang boleh dilewati oleh paket sebelum dihancurkan agar tidak berputar-putar selamanya di internet. Setiap kali paket melewati satu router, nilai TTL akan dikurangi 1.
> 
> Karena setiap OS menetapkan nilai awal TTL yang berbeda, kita bisa menebak OS target:
> 
> - Nilai awal **Linux** umumnya **64**.
>     
> - Nilai awal **Windows** umumnya **128**.
>     
> 
> _Contoh:_ Jika Anda menerima balasan dengan nilai `ttl=58`, ini mengindikasikan bahwa target aslinya adalah mesin **Linux** ($64$) yang berada **6 router jauhnya** dari Anda ($64 - 6 = 58$).

### Kasus Gagal: Tidak Ada Balasan (No Reply)

Jika Anda melihat pesan seperti `"Destination Host Unreachable"` atau terjadi _100% packet loss_ tanpa pesan eror sama sekali, ada beberapa faktor yang menyebabkannya:

1. **Pemblokiran oleh Windows Firewall:** Secara bawaan (_default_), **Windows Firewall akan memblokir semua paket ICMP masuk** (`Inbound Echo Request`). Ini adalah fitur keamanan bawaan dari Microsoft agar komputer Windows tidak mudah dideteksi dan dipetakan oleh penyerang di internet (_Security via Obscurity_).
    
2. **Keamanan Cloud & Perusahaan:** Penyedia layanan cloud (seperti AWS, Azure, GCP) serta _Web Application Firewall_ (WAF) modern biasanya mematikan fungsi tanggapan ICMP sepenuhnya demi mencegah pengintaian awal.
    
3. **Kondisi Fisik:** Komputer target memang dalam keadaan mati (_power off_), sedang _crash_, atau mengalami kegagalan rute jaringan.
    

## 4. Tabel Ringkasan Analisis Jaringan

| **Hasil Analisis Ping**                | **Arti yang Paling Memungkinkan**                                         | **Langkah Aksi Selanjutnya**                                                      |
| -------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Balasan cepat, _packet loss_ 0%        | Target aktif, _online_, dan membuka akses ICMP.                           | Lanjutkan reconnaissance ke tahap _port scanning_ (misal dengan Nmap).            |
| _Destination Host Unreachable_         | Mesin target mati atau tidak ada jalur rute logis menuju ke sana.         | Periksa konfigurasi jaringan atau pastikan mesin target sudah menyala.            |
| _100% packet loss_ (Hening)            | ICMP disaring/diblokir oleh Firewall (seperti Windows Firewall) atau WAF. | Gunakan metode _host discovery_ lain yang berbasis TCP/UDP (misalnya `nmap -Pn`). |
| Latensi melonjak tinggi / tidak stabil | Terjadi kemacetan parah di jalur jaringan (_network congestion_).         | Analisis rute perjalanan paket secara detail menggunakan perintah `traceroute`.   |

## Telnet

Dalam dunia _cybersecurity_, **Active Reconnaissance** adalah tahap di mana kita berinteraksi langsung dengan target untuk mengumpulkan informasi. Salah satu teknik paling dasar namun sangat berguna adalah **Banner Grabbing** (mengambil spanduk informasi).

### 1. Apa itu Protokol TELNET?

- **Definisi:** Dikembangkan tahun 1969, Telnet (_Teletype Network_) adalah protokol lama yang digunakan untuk mengontrol atau berkomunikasi dengan komputer jarak jauh via baris perintah (_Command Line_).
    
- **Port Default:** `23`
    
- **Masalah Keamanan:** Telnet mengirimkan data (termasuk _username_ dan _password_) dalam bentuk **teks biasa (plain text)** tanpa enkripsi. Siapa pun yang menyadap jaringan bisa mencuri data tersebut.
    
- **Solusi Modern:** Sekarang kita menggunakan **SSH (Secure Shell)** yang jauh lebih aman karena mendefinisikan enkripsi untuk semua data.
    

### 2. Kenapa Telnet Dipakai untuk _Reconnaissance_?

Meskipun sudah tidak aman untuk administrasi, klien Telnet sangat berguna untuk _pentesting_. Karena Telnet berjalan di atas protokol **TCP**, kita bisa menggunakannya untuk mengetuk/terhubung ke port TCP mana saja dan melihat respons dari server tersebut.

Teknik ini disebut **Banner Grabbing**.

> **Banner** adalah pesan atau respons awal yang dikirimkan oleh server saat ada koneksi masuk. Banner ini sering kali membocorkan **nama perangkat lunak** dan **versi spesifik** yang sedang berjalan di port tersebut.

### 3. Cara Instalasi

Jika Telnet belum ada di sistem Linux kamu (seperti Kali Linux, Debian, atau Ubuntu), kamu bisa menginstalnya dengan perintah:

Bash

```
sudo apt install telnet
```

_Catatan: Alat lain seperti `netcat` (`nc`) atau `curl` juga sering digunakan sebagai alternatif karena lebih fleksibel._

### 4. Praktek: Banner Grabbing pada Web Server (Port 80)

Misalkan kita ingin memeriksa web server target menggunakan IP: `MACHINE_IP` pada port `80` (HTTP).

#### Langkah-langkahnya:

1. Hubungkan Telnet ke port 80 target.
    
2. Kirim permintaan (request) HTTP minimal secara manual agar server memberikan respons.
    

#### Contoh di Terminal:

Bash

```
pentester@TryHackMe$ telnet MACHINE_IP 80
Trying MACHINE_IP...
Connected to MACHINE_IP.
Escape character is '^]'.

# Ketik perintah di bawah ini secara manual, lalu tekan ENTER 2x:
GET / HTTP/1.1
host: telnet

# Server akan memberikan respons seperti ini:
HTTP/1.1 200 OK
Server: nginx/1.6.2
Date: Tue, 17 Aug 2021 11:13:25 GMT
Content-Type: text/html
Content-Length: 867
Last-Modified: Tue, 17 Aug 2021 11:12:16 GMT
Connection: keep-alive
ETag: "611b9990-363"
Accept-Ranges: bytes
...
```

#### Informasi Penting yang Didapat:

Perhatikan baris ini:

> `Server: nginx/1.6.2`

Dari informasi ini, kita tahu bahwa target menggunakan web server **Nginx versi 1.6.2**.

**Apa langkah selanjutnya bagi seorang Pentester?**

Informasi versi ini bisa kita cari di database kerentanan seperti **CVE (Common Vulnerabilities and Exposures)** atau **Exploit-DB** untuk melihat apakah versi tersebut memiliki celah keamanan (vulnerability) yang bisa dieksploitasi.

### 5. Banner Grabbing pada Layanan Lain

Konsep ini berlaku untuk semua layanan berbasis TCP:

- **FTP (Port 21):** Biasanya langsung mengirimkan banner berisi versi aplikasi sesaat setelah kita terhubung, tanpa perlu mengetikkan perintah apa pun.
    
- **Email (SMTP/POP3):** Kita bisa terhubung dan menggunakan perintah khusus protokol email untuk meminta informasi.
    

### 6. Bagaimana Jika Layanannya Menggunakan Enkripsi (HTTPS/TLS)?

Telnet **tidak bisa** membaca atau menangani koneksi yang terenkripsi. Jika target menggunakan port terenkripsi seperti HTTPS (Port 443) atau SMTPS (Port 465), kita harus menggunakan alat lain:

- **Untuk HTTPS:**
    
    Bash
    
    ```
    curl --head https://MACHINE_IP
    ```
    
    atau
    
    Bash
    
    ```
    openssl s_client -connect MACHINE_IP:443
    ```
    
- **Untuk layanan TLS lainnya:** Gunakan `openssl s_client` atau `ncat --ssl`.
    

_Tips Belajar: Saat kamu melakukan praktik di lab TryHackMe, output versi server mungkin akan berbeda karena setiap mesin target dikonfigurasi secara unik. Selalu perhatikan bagian baris "Server:" atau spanduk awal yang muncul!_

## Netcat

Jika sebelumnya kita menggunakan Telnet, sekarang kita akan mempelajari **Netcat (`nc`)**. Netcat sering dijuluki sebagai _"Swiss Army Knife"_ (Pisau Lipat Swiss) dalam dunia jaringan karena fungsinya yang sangat serbaguna.

### 1. Apa itu Netcat (`nc`)?

Netcat adalah perkakas jaringan yang mendukung protokol **TCP** dan **UDP**. Kehebatan utama Netcat adalah sifat ganda (_dual-capability_) miliknya:

- **Sebagai Klien:** Bisa terhubung ke port yang sedang terbuka di komputer lain (mirip Telnet).
    
- **Sebagai Server:** Bisa membuka port di komputer sendiri dan menunggu koneksi masuk (_listening_).
    

> **Versi Modern (`ncat`):** Bagian dari proyek Nmap. `ncat` memiliki fitur lebih canggih seperti mendukung IPv6 dan enkripsi SSL/TLS, membuatnya jauh lebih unggul dibandingkan Telnet lama yang tidak aman.

### 2. Mengambil Banner (_Banner Grabbing_) dengan Netcat

Cara kerja pengambilan banner menggunakan Netcat sama persis dengan Telnet. Sintaks dasarnya adalah:

Bash

```
nc [IP_TARGET] [PORT]
```

#### Contoh Praktik pada Web Server (Port 80):

1. Jalankan perintah koneksi di terminal.
    
2. Masukkan perintah HTTP secara manual (Tips: Tekan `Shift + Enter` setelah mengetik baris `GET` jika diperlukan, lalu tekan **Enter 2x** di akhir untuk mengeksekusi).
    

Bash

```
pentester@TryHackMe$ nc 10.48.182.85 80
GET / HTTP/1.1
host: netcat

# Respons dari server:
HTTP/1.1 200 OK
Server: nginx/1.6.2
Date: Tue, 17 Aug 2021 11:39:49 GMT
Content-Type: text/html
Content-Length: 867
...
```

Sama seperti sebelumnya, kita berhasil mendapatkan informasi berharga: **Server: nginx/1.6.2**.

#### Pada Layanan Lain:

- **FTP (Port 21):** Cukup ketik `nc 10.48.182.85 21`, banner versi FTP akan langsung muncul otomatis tanpa perlu mengetik perintah tambahan.
    
- **SMTP (Port 25):** Menghubungkan ke port ini akan langsung menampilkan identitas dari server email target.
    

### 3. Menggunakan Netcat sebagai Server (_Listening_)

Selain mengintip port orang lain, Netcat bisa digunakan untuk membuka pintu di komputer kita sendiri. Ini berguna untuk menguji koneksi, mentransfer file, atau membuat ruang obrolan (_chat_) sederhana antar komputer.

#### Langkah-langkah Membuat Koneksi 2 Komputer:

1. **Di Sisi Server (Komputer yang Menunggu):**
    
    Jalankan perintah untuk mendengarkan (_listening_) pada port tertentu (misalnya port 1234):
    
    Bash
    
    ```
    nc -vnlp 1234
    ```
    
2. **Di Sisi Klien (Komputer yang Menghubungkan):**
    
    Hubungkan ke IP server dan port yang dibuka tadi:
    
    Bash
    
    ```
    nc 10.48.182.85 1234
    ```
    

_Setelah terhubung, apa pun yang kamu ketik di terminal server akan muncul di terminal klien, dan sebaliknya._

### 4. Tabel Arti _Flag_ / Opsi pada Perintah `nc -vnlp`

Untuk mempermudah ingatanmu, berikut adalah arti dari kombinasi _flag_ `-vnlp`:

| **Opsi / Flag** | **Arti & Fungsi**                                                                                                                                        |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`-l`**        | **Listen:** Mengubah Netcat menjadi mode server untuk mendengarkan koneksi masuk.                                                                        |
| **`-p`**        | **Port:** Menentukan nomor port yang ingin digunakan. _(Penting: nomor port harus ditulis tepat setelah flag -p ini, misal: `-p 1234`)_.                 |
| **`-n`**        | **Numeric-only:** Hanya menggunakan angka IP. Netcat tidak akan membuang waktu untuk mencari nama domain (DNS Resolution), sehingga koneksi lebih cepat. |
| **`-v`**        | **Verbose:** Menampilkan detail informasi proses yang terjadi (sangat berguna untuk melacak error/debugging).                                            |
| **`-vv`**       | **Very Verbose:** Memberikan informasi yang jauh lebih detail lagi dari `-v`.                                                                            |
| **`-k`**        | **Keep-open:** Menjaga port server tetap terbuka dan mendengarkan, bahkan setelah klien pertama memutuskan koneksi.                                      |

### ⚠️ Catatan Penting & Tips Keamanan

- **Hak Akses Root:** Jika kamu ingin membuka port di bawah **1024** (seperti port 80, 21, 443), kamu wajib menggunakan perintah `sudo` karena port tersebut membutuhkan hak akses Administrator/Root.
    
- **Penggunaan IPv6:** Jika jaringan target menggunakan IPv6, tambahkan flag `-6`. Contoh: `nc -6 -lp 1234`.
    
- **Enkripsi Data:** Data yang dikirim via Netcat standar (`nc`) tidak terenkripsi. Jika kamu mentransfer data sensitif, gunakan `ncat --ssl` agar komunikasi aman dari penyadapan.
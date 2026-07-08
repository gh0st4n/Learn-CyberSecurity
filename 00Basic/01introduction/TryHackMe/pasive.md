# Passive Reconnaissance Room

## Penjelasan
Passive Reconnaissance adalah kegiatan mencari informasi dari publik tanpa berkomunikasi/kontak langsung dengan target. Passive Reconnaissance adalah Fase Paling Ampuh dan Paling Rendah Resiko.

Reconnaissance(Recon) adalah survei pendahuluan untuk mengumpulkan informasi tentang target. Ini tetap menjadi fase pertama dalam kerangka serangan modern seperti Unified Kill Chain (di mana pengintaian membantu mendapatkan pemahaman awal sebelum menyentuh apa pun) dan variasi dari Cyber ​​Kill Chain klasik. Reconnaissance terbagi menjadi dua jenis utama(Passive & Active).

## Objektifitas
1. Menggunakan **Whois** untuk informasi Registrasi Domain
2. **dig** dan **nslookup** untuk mencari informasi record DNS
3. Memahami mengapa query **WHOIS** dan **DNS** dianggap Pasif
4. Temukan subdomain menggunakan DNSDumpster dan log Certificate Transparency.
5. Kumpulkan informasi intelijen tentang layanan yang terekspos menggunakan Shodan.io.

## Persyaratan
1. Networking
2. Linux Fundamental

## Passive Reconnaissance
Passive Reconnaissance sepenuhnya bergantung pada informasi yang tersedia untuk umum. Tidak ada paket data yang dikirim ke target dan tidak ada interaksi langsung yang terjadi. Ini analog dengan mengamati wilayah target dari jarak aman menggunakan teropong, tanpa pernah menginjakkan kaki di tanah mereka.

### Aktivitas passive yang umum meliputi:

1. Mengakses catatan DNS publik dari resolver terbuka (A, MX, TXT, dll.).
2. Mencari subdomain dan sertifikat yang diterbitkan dalam log transparansi sertifikat (misalnya, crt.sh).
3. Meninjau lowongan pekerjaan di LinkedIn atau halaman karier perusahaan untuk mendapatkan petunjuk tentang tumpukan teknologi (tech stack).
4. Membaca berita publik, siaran pers, atau dokumen yang bocor di situs-situs berbagi informasi.
5. Memeriksa perangkat yang terekspos melalui mesin pencari seperti Shodan atau Censys.
6. Memindai repositori GitHub publik untuk mencari kredensial atau file konfigurasi yang dikodekan secara permanen.


## Active Reconnaissance
Active Reconnaissance memerlukan keterlibatan langsung dengan target. Data yang anda kirimkan dapat dicatat, dideteksi, atau diblokir. Ini analog dengan berjalan ke pintu dan jendela untuk menguji kunci, kamera, dan alarm.

### Aktivitas aktif umum meliputi:

1. Mengirim paket untuk menemukan host yang aktif (misalnya, ICMP ping, ARP Requests).
2. Port Scanning atau Service Enumeartion(Nmap, masscan).
3. Berinteraksi dengan aplikasi web atau API (fuzzing endpoint, brute-forcing direktori).
4. Social Engineering (phishing, panggilan telepon dengan tipu daya/penipuan).
5. Pendekatan fisik (mengikuti kendaraan dari dekat, berpura-pura sebagai penjual/vendor).


## WHOIS
WHOIS adalah protokol permintaan/respons yang didefinisikan dalam [3912](https://www.ietf.org/rfc/rfc3912.txt). Server WHOIS mendengarkan pada TCP port 43 dan menyediakan detail pendaftaran untuk nama domain. **Pendaftar Domain** memelihara catatan ini untuk domain yang mereka sewakan.

Dari respons WHOIS, detail berikut mungkin tersedia (jika tidak disensor):

- Registrar: Perusahaan (misalnya, Namecheap, GoDaddy) yang mendaftarkan domain tersebut.
- Informasi kontak pendaftar: Nama, organisasi, alamat, telepon, dan email. Namun, layanan privasi (standar sejak 2018) biasanya menggantinya dengan "Dirahasiakan untuk Privasi" atau yang serupa.
- Tanggal: Pembuatan (pendaftaran), Pembaruan (perubahan terakhir), dan Kedaluwarsa (batas waktu perpanjangan).
- Names Server: Server yang berwenang untuk domain tersebut.
- Kode status: Misalnya, clientTransferProhibited menunjukkan bahwa domain tersebut terkunci terhadap transfer yang tidak sah.
- Kontak untuk pelaporan penyalahgunaan: Alamat email dan nomor telepon petugas registrasi untuk melaporkan masalah.

**Syntax** : whois DOMAIN_NAME

```bash
┌─[gh0st4n@Gh0sT4n]─[~]
└──╼$ whois tryhackme.com
   Domain Name: TRYHACKME.COM
   Registry Domain ID: 2282723194_DOMAIN_COM-VRSN
   Registrar WHOIS Server: whois.namecheap.com
   Registrar URL: http://www.namecheap.com
   Updated Date: 2025-05-11T14:06:02Z
   Creation Date: 2018-07-05T19:46:15Z
   Registry Expiry Date: 2034-07-05T19:46:15Z
   Registrar: NameCheap, Inc.
   Registrar IANA ID: 1068
   Registrar Abuse Contact Email: abuse@namecheap.com
   Registrar Abuse Contact Phone: +1.6613102107
   Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited
   Name Server: KIP.NS.CLOUDFLARE.COM
   Name Server: UMA.NS.CLOUDFLARE.COM
   DNSSEC: unsigned
   URL of the ICANN Whois Inaccuracy Complaint Form: https://www.icann.org/wicf/
>>> Last update of whois database: 2026-07-06T13:53:47Z <<<

For more information on Whois status codes, please visit https://icann.org/epp

NOTICE: The expiration date displayed in this record is the date the
registrar's sponsorship of the domain name registration in the registry is
currently set to expire. This date does not necessarily reflect the expiration
date of the domain name registrant's agreement with the sponsoring
registrar.  Users may consult the sponsoring registrar's Whois database to
view the registrar's reported date of expiration for this registration.

TERMS OF USE: You are not authorized to access or query our Whois
database through the use of electronic processes that are high-volume and
automated except as reasonably necessary to register domain names or
modify existing registrations; the Data in VeriSign Global Registry
Services' ("VeriSign") Whois database is provided by VeriSign for
information purposes only, and to assist persons in obtaining information
about or related to a domain name registration record. VeriSign does not
guarantee its accuracy. By submitting a Whois query, you agree to abide
by the following terms of use: You agree that you may use this Data only
for lawful purposes and that under no circumstances will you use this Data
to: (1) allow, enable, or otherwise support the transmission of mass
unsolicited, commercial advertising or solicitations via e-mail, telephone,
or facsimile; or (2) enable high volume, automated, electronic processes
that apply to VeriSign (or its computer systems). The compilation,
repackaging, dissemination or other use of this Data is expressly
prohibited without the prior written consent of VeriSign. You agree not to
use electronic processes that are automated and high-volume to access or
query the Whois database except as reasonably necessary to register
domain names or modify existing registrations. VeriSign reserves the right
to restrict your access to the Whois database in its sole discretion to ensure
operational stability.  VeriSign may restrict or terminate your access to the
Whois database for failure to abide by these terms of use. VeriSign
reserves the right to modify these terms at any time.

The Registry database contains ONLY .COM, .NET, .EDU domains and
Registrars.
Domain name: tryhackme.com
Registry Domain ID: 2282723194_DOMAIN_COM-VRSN
Registrar WHOIS Server: whois.namecheap.com
Registrar URL: http://www.namecheap.com
Updated Date: 2025-05-11T14:06:03.00Z
Creation Date: 2018-07-05T19:46:15.00Z
Registrar Registration Expiration Date: 2034-07-05T19:46:15.00Z
Registrar: NAMECHEAP INC
Registrar IANA ID: 1068
Registrar Abuse Contact Email: abuse@namecheap.com
Registrar Abuse Contact Phone: +1.9854014545
Reseller: NAMECHEAP INC
Domain Status: clientTransferProhibited https://icann.org/epp#clientTransferProhibited
Registry Registrant ID: 
Registrant Name: Redacted for Privacy
Registrant Organization: Privacy service provided by Withheld for Privacy ehf
Registrant Street: Kalkofnsvegur 2 
Registrant City: Reykjavik
Registrant State/Province: Capital Region
Registrant Postal Code: 101
Registrant Country: IS
Registrant Phone: +354.4212434
Registrant Phone Ext: 
Registrant Fax: 
Registrant Fax Ext: 
Registrant Email: a70a4ff6d25041a48378997194f9e834.protect@withheldforprivacy.com
Registry Admin ID: 
Admin Name: Redacted for Privacy
Admin Organization: Privacy service provided by Withheld for Privacy ehf
Admin Street: Kalkofnsvegur 2 
Admin City: Reykjavik
Admin State/Province: Capital Region
Admin Postal Code: 101
Admin Country: IS
Admin Phone: +354.4212434
Admin Phone Ext: 
Admin Fax: 
Admin Fax Ext: 
Admin Email: a70a4ff6d25041a48378997194f9e834.protect@withheldforprivacy.com
Registry Tech ID: 
Tech Name: Redacted for Privacy
Tech Organization: Privacy service provided by Withheld for Privacy ehf
Tech Street: Kalkofnsvegur 2 
Tech City: Reykjavik
Tech State/Province: Capital Region
Tech Postal Code: 101
Tech Country: IS
Tech Phone: +354.4212434
Tech Phone Ext: 
Tech Fax: 
Tech Fax Ext: 
Tech Email: a70a4ff6d25041a48378997194f9e834.protect@withheldforprivacy.com
Name Server: kip.ns.cloudflare.com
Name Server: uma.ns.cloudflare.com
DNSSEC: unsigned
URL of the ICANN WHOIS Data Problem Reporting System: http://wdprs.internic.net/
>>> Last update of WHOIS database: 2026-07-06T10:43:17.91Z <<<
For more information on Whois status codes, please visit https://icann.org/epp
```

**RDAP example**
Gunakan curl untuk melakukan query ke endpoint RDAP publik (misalnya, Verisign untuk domain **.com**). Utilitas jq memformat output JSON agar mudah dibaca; utilitas ini sudah terinstal di AttackBox. Jika Anda menggunakan sistem sendiri, instal melalui pengelola paket Anda (misalnya, sudo apt install jq).

```bash
┌─[gh0st4n@Gh0sT4n]─[~]
└──╼$ curl -s https://rdap.verisign.com/com/v1/domain/tryhackme.com | jq .
{
  "objectClassName": "domain",
  "handle": "2282723194_DOMAIN_COM-VRSN",
  "ldhName": "TRYHACKME.COM",
  "links": [
    {
      "value": "https://rdap.verisign.com/com/v1/domain/TRYHACKME.COM",
      "rel": "self",
      "href": "https://rdap.verisign.com/com/v1/domain/TRYHACKME.COM",
      "type": "application/rdap+json"
    },
    {
      "value": "https://rdap.namecheap.com/domain/TRYHACKME.COM",
      "rel": "related",
      "href": "https://rdap.namecheap.com/domain/TRYHACKME.COM",
      "type": "application/rdap+json"
    }
  ],
  "status": [
    "client transfer prohibited"
  ],
  "entities": [
    {
      "objectClassName": "entity",
      "handle": "1068",
      "roles": [
        "registrar"
      ],
      "links": [
        {
          "href": "http://www.namecheap.com",
          "type": "text/html",
          "value": "https://rdap.namecheap.com/",
          "rel": "about"
        }
      ],
      "publicIds": [
        {
          "type": "IANA Registrar ID",
          "identifier": "1068"
        }
      ],
      "vcardArray": [
        "vcard",
        [
          [
            "version",
            {},
            "text",
            "4.0"
          ],
          [
            "fn",
            {},
            "text",
            "NameCheap, Inc."
          ]
        ]
      ],
      "entities": [
        {
          "objectClassName": "entity",
          "roles": [
            "abuse"
          ],
          "vcardArray": [
            "vcard",
            [
              [
                "version",
                {},
                "text",
                "4.0"
              ],
              [
                "fn",
                {},
                "text",
                ""
              ],
              [
                "tel",
                {
                  "type": "voice"
                },
                "uri",
                "tel:+1.6613102107"
              ],
              [
                "email",
                {},
                "text",
                "abuse@namecheap.com"
              ]
            ]
          ]
        }
      ]
    }
  ],
  "events": [
    {
      "eventAction": "registration",
      "eventDate": "2018-07-05T19:46:15Z"
    },
    {
      "eventAction": "expiration",
      "eventDate": "2034-07-05T19:46:15Z"
    },
    {
      "eventAction": "last changed",
      "eventDate": "2025-05-11T14:06:02Z"
    },
    {
      "eventAction": "last update of RDAP database",
      "eventDate": "2026-07-06T13:56:47Z"
    }
  ],
  "secureDNS": {
    "delegationSigned": false
  },
  "nameservers": [
    {
      "objectClassName": "nameserver",
      "ldhName": "KIP.NS.CLOUDFLARE.COM"
    },
    {
      "objectClassName": "nameserver",
      "ldhName": "UMA.NS.CLOUDFLARE.COM"
    }
  ],
  "rdapConformance": [
    "rdap_level_0",
    "icann_rdap_technical_implementation_guide_1",
    "icann_rdap_response_profile_1"
  ],
  "notices": [
    {
      "title": "Terms of Service",
      "description": [
        "Service subject to Terms of Use."
      ],
      "links": [
        {
          "href": "https://www.verisign.com/domain-names/registration-data-access-protocol/terms-service/index.xhtml",
          "type": "text/html",
          "value": "https://rdap.verisign.com/com/v1/domain/tryhackme.com",
          "rel": "terms-of-service"
        }
      ]
    },
    {
      "title": "Status Codes",
      "description": [
        "For more information on domain status codes, please visit https://icann.org/epp"
      ],
      "links": [
        {
          "href": "https://icann.org/epp",
          "type": "text/html"
        }
      ]
    },
    {
      "title": "RDDS Inaccuracy Complaint Form",
      "description": [
        "URL of the ICANN RDDS Inaccuracy Complaint Form: https://icann.org/wicf"
      ],
      "links": [
        {
          "href": "https://icann.org/wicf",
          "type": "text/html",
          "value": "https://rdap.verisign.com/com/v1/domain/tryhackme.com",
          "rel": "help"
        }
      ]
    }
  ]
}
```

**What to look for**:

- Redirection chain (Verisign to registrar server).
- Dates: useful for estimating company age or identifying renewal phishing windows.
- Name servers: potential new targets (if in scope).
- Status: locked domains (e.g., `clientTransferProhibited`) are harder to hijack.

**Online alternatives** (if the `whois` command behaves unexpectedly):

- https://whois.icann.org/ (legacy WHOIS)
- https://lookup.icann.org/ (modern RDAP-focused lookup)
- https://www.whoxy.com/ (historical WHOIS snapshots, free limited use)

## nslookup & dig
Tugas ini memperkenalkan dua hal alat kueri: nslookup Dan digKeduanya melakukan kueri DNS, tetapi dig(secara historis merupakan akronim balik untuk "Domain Information Groper") adalah pilihan modern yang lebih disukai. Ini memberikan output yang lebih bersih, menampilkan nilai TTL secara default (menunjukkan berapa lama catatan di-cache), dan lebih andal untuk kueri dan skrip yang kompleks. nslookupHal ini dibahas di sini untuk alasan kompatibilitas, karena Anda akan menemukannya dalam dokumentasi lama dan pada sistem Windows, tetapi digSeharusnya ini menjadi alat default Anda.

### nslookup
**nslookup**(Name Server Lookup) tool lama

Syntax :
- **nslookup DOMAIN_NAME** melakukan pencarian sederhana menggunakan resolver default Anda.
- **nslookup -type=TYPE DOMAIN_NAME [SERVER]** Menentukan tipe record dan server DNS opsional.

Jenis-jenis record DNS umum:

| Jenis kueri | Hasil                                                                                            |
| ----------- | ------------------------------------------------------------------------------------------------ |
| A           | Alamat IPv4 untuk domain tersebut                                                                |
| AAAA        | Alamat IPv6 untuk domain tersebut                                                                |
| CNAME       | Nama Kanonik: alias yang mengarahkan satu nama domain ke nama domain lainnya.                    |
| MX          | Mail Server: server yang bertanggung jawab untuk menangani email untuk domain tersebut.          |
| SOA         | Start of Authority : server nama utama, email admin, dan nomor seri zona.                        |
| TXT         | TXT Records : Teks sembarang, yang umum digunakan untuk SPF, DKIM, DMARC, dan verifikasi domain. |

Contoh (IPv4 address via Cloudflare's resolver)
```bash
┌─[gh0st4n@Gh0sT4n]─[~]
└──╼$ nslookup -type=A tryhackme.com 1.1.1.1
Server:		1.1.1.1
Address:	1.1.1.1#53

Non-authoritative answer:
Name:	tryhackme.com
Address: 64.239.123.193
Name:	tryhackme.com
Address: 64.239.109.193
```

IP ini seringkali berupa anycast (Cloudflare dalam kasus ini). Untuk pengujian penetrasi, setiap IP dapat menampung layanan yang berbeda, jadi periksa apakah IP tersebut termasuk dalam cakupan pengujian.

Contoh MX(Mail Server)
```
┌─[gh0st4n@Gh0sT4n]─[~]
└──╼$ nslookup -type=MX tryhackme.com
Server:		xx.xx.xxx.xx
Address:	xx.xx.xxx.xx#53

Non-authoritative answer:
tryhackme.com	mail exchanger = 1 aspmx.l.google.com.
tryhackme.com	mail exchanger = 10 alt3.aspmx.l.google.com.
tryhackme.com	mail exchanger = 10 alt4.aspmx.l.google.com.
tryhackme.com	mail exchanger = 5 alt1.aspmx.l.google.com.
tryhackme.com	mail exchanger = 5 alt2.aspmx.l.google.com.

Authoritative answers can be found from:
```

## dig
**dig** adalah alat query DNS modern yang lebih disukai.

Syntax : **dig [@SERVER] DOMAIN_NAME [TYPE]**

Contoh (MX Record via Cloudflare)

```bash
┌─[gh0st4n@Gh0sT4n]─[~]
└──╼$ dig @1.1.1.1 tryhackme.com MX

; <<>> DiG 9.20.23-1~deb13u1-Debian <<>> @1.1.1.1 tryhackme.com MX
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 53521
;; flags: qr rd ra; QUERY: 1, ANSWER: 5, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;tryhackme.com.			IN	MX

;; ANSWER SECTION:
tryhackme.com.		300	IN	MX	1 aspmx.l.google.com.
tryhackme.com.		300	IN	MX	10 alt3.aspmx.l.google.com.
tryhackme.com.		300	IN	MX	10 alt4.aspmx.l.google.com.
tryhackme.com.		300	IN	MX	5 alt1.aspmx.l.google.com.
tryhackme.com.		300	IN	MX	5 alt2.aspmx.l.google.com.

;; Query time: 86 msec
;; SERVER: 1.1.1.1#53(1.1.1.1) (UDP)
;; WHEN: Tue Jul 07 20:43:29 WIB 2026
;; MSG SIZE  rcvd: 157
```

Privisi Tip : Gunakan resolver publik seperti 1.1.1.1 (yang mendukung DNS melalui HTTPS dan DNS melalui TLS) untuk menghindari ISP Anda mencatat query Anda.

## DNSDumpter

Standar DS pencarian ( `dig`/ `nslookup`) hanya akan menyelesaikan nama yang sudah Anda ketahui. Mereka tidak akan mengungkapkan subdomain yang tidak diiklankan seperti `blog.tryhackme.com`, `app.tryhackme.com`, atau `dev.internal.company.com`.

Subdomain penting karena sering kali mengekspos layanan yang terlupakan atau rentan (instalasi CMS yang sudah usang, panel pengembangan), IT bayangan atau aplikasi yang salah konfigurasi, dan permukaan serangan tambahan seperti API yang terekspos atau portal admin.

Dalam pengintaian pasif, subdomain ini ditemukan menggunakan sumber OSINT publik tanpa mengirimkan kueri apa pun ke target.

Salah satu alat gratis yang terkenal adalah **[DNSDumpster](https://dnsdumpster.com/)** . Alat ini mengumpulkan data DNS publik dari berbagai sumber seperti cache mesin pencari, basis data transfer zona, dan catatan sertifikat. Alat ini tidak melakukan enumerasi paksa, yang berarti tetap sepenuhnya pasif. Hasilnya mencakup subdomain dan host, IP yang telah diresolusi dengan geolokasi, catatan MX, TXT, dan CNAME, serta peta visual yang menunjukkan hubungan di antara semuanya.

Cari `tryhackme.com`di DNSDumpster dan Anda akan melihat entri seperti `blog.tryhackme.com`Pencarian DNS dasar tidak dapat melewatkannya.

DNSDumpster juga membuat grafik data, yang menunjukkan bagaimana subdomain, IP, dan server email saling berhubungan

### Certificate Transparency (CT) Log

Metode penemuan subdomain pasif yang paling efektif saat ini adalah **log Transparansi Sertifikat** , yang dapat diakses melalui **[crt.sh](https://crt.sh)**.

**Certificate Transparency** adalah kerangka kerja pencatatan publik (wajib sejak sekitar tahun 2015) yang mencatat setiap sertifikat SSL/TLS yang dikeluarkan oleh Otoritas Sertifikat yang berpartisipasi. Setiap sertifikat berisi **bidang Subject Alternative Name (SAN)** yang mencantumkan domain dan subdomain yang dicakupnya. Dengan mencari di log ini, Anda dapat menemukan subdomain tanpa mengirimkan lalu lintas apa pun ke target.

Untuk menggunakan crt.sh, kunjungi `https://crt.sh`dan mencari `%.tryhackme.com`. Itu `%` Karakter wildcard cocok dengan subdomain apa pun. Hasilnya akan mencantumkan setiap sertifikat yang diterbitkan untuk subdomain dari `tryhackme.com`, seringkali mengungkap 10 hingga 100 kali lebih banyak subdomain daripada DNSDumpster saja.

crt.sh sepenuhnya pasif, beroperasi secara real-time, dan tidak memiliki batasan laju untuk penggunaan dasar.

Opsi penemuan subdomain pasif lainnya termasuk SecurityTrails (pencarian terbatas gratis) dan alat baris perintah seperti Subfinder, yang menggabungkan beberapa sumber pasif.


## Shodan

**Shodan** adalah mesin pencari untuk perangkat yang terhubung ke internet. Ia terus-menerus memindai internet publik, mengumpulkan banner dan respons dari port dan layanan terbuka, dan mengindeksnya untuk pencarian. Tidak seperti Google, yang mengindeks halaman web, Shodan berfokus pada perangkat: server, peralatan, kamera, router, sistem kontrol industri, dan banyak lagi.

**Nilai defensif** : Organisasi memantau Shodan (melalui peringatan atau pemeriksaan manual) untuk mengidentifikasi kerentanan yang tidak disengaja seperti server nakal, mesin uji yang terlupakan, atau layanan yang rentan.

### Menavigasi Antarmuka Shodan

Untuk memulai, kunjungi `https://www.shodan.io`Tidak diperlukan akun untuk pencarian dasar. Masukkan nama domain (misalnya, `tryhackme.com`) atau alamat IP dari pencarian DNS Anda sebelumnya (misalnya, `104.26.10.229`) ke dalam bilah pencarian.

Halaman hasil menampilkan daftar host yang cocok. Memilih host akan membuka tampilan detail yang berisi informasi berikut:

- **Alamat IP** dan **ASN** (Autonomous System Number): mengidentifikasi blok jaringan.
- **Penyedia/organisasi hosting** (misalnya, Cloudflare, AWS): mengungkapkan infrastruktur di balik domain tersebut.
- **Lokasi geografis** (negara, kota): perkiraan lokasi fisik server.
- **Port dan layanan yang terbuka** : dengan string versi dan banner (misalnya, tipe dan versi server HTTP).
- **Tag** : seperti `cdn` atau `vuln`jika kerentanan yang diketahui sesuai dengan versi layanan yang terdeteksi.

### Tips Pencarian

Shodan mendukung berbagai filter pencarian untuk mempersempit hasil:

- `hostname:tryhackme.com`cocok dengan nama host tertentu.
- `org:"TryHackMe"`Filter berdasarkan nama organisasi.
- `port:443 country:US`Filter berdasarkan pelabuhan dan negara.
- `http.component:"wordpress"`Mengidentifikasi tumpukan teknologi (jika terekspos).

Untuk referensi lengkap, lihat: https://help.shodan.io/the-basics/search-query-fundamentals

Untuk eksplorasi lebih lanjut, **[Censys.io (buka di tab baru)](https://search.censys.io/)** (pencarian dasar gratis) menyediakan data host dan sertifikat serupa. Ini dapat berfungsi sebagai pelengkap yang berguna saat melakukan referensi silang hasil.

### Tip

- Gunakan resolver DoH/DoT (misalnya, `1.1.1.1`) untuk menjaga kerahasiaan pertanyaan Anda.
- Sebagai pihak yang bertugas membela diri, pantau jejak digital Anda: atur peringatan Shodan/Censys, perhatikan log CT untuk sertifikat baru, dan lacak aktivitas peretasan. perubahan untuk risiko pengambilalihan.
- Meskipun pengintaian pasif tidak menyentuh target secara langsung, selalu pastikan keterlibatan Anda secara keseluruhan telah diotorisasi dan sesuai dengan ruang lingkup yang ditentukan.
- Hasilnya berubah seiring waktu. Rotasi (Cloudflare anycast), subdomain muncul dan menghilang, dan pengeditan privasi meningkat.
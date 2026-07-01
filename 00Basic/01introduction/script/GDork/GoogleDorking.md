# Cheatsheet Google Dorking

## Filter Pencarian

|**Filter**|**Deskripsi**|**Contoh**|
|---|---|---|
|**allintext**|Mencari halaman yang memuat _semua_ kata kunci yang diberikan di dalam teks halaman.|`allintext:"kata kunci"`|
|**intext**|Mencari kemunculan kata kunci di dalam teks (bisa sekaligus atau satu per satu).|`intext:"kata kunci"`|
|**inurl**|Mencari URL yang mengandung salah satu kata kunci.|`inurl:"kata kunci"`|
|**allinurl**|Mencari URL yang mengandung _semua_ kata kunci yang ada dalam kueri.|`allinurl:"kata kunci"`|
|**intitle**|Mencari kata kunci di dalam judul halaman (bisa salah satu atau semua).|`intitle:"kata kunci"`|
|**allintitle**|Mencari halaman yang judulnya memuat _semua_ kata kunci sekaligus.|`allintitle:"kata kunci"`|
|**site**|Membatasi pencarian hanya pada situs web atau domain tertentu.|`site:"www.google.com"`|
|**filetype**|Mencari format atau jenis file spesifik yang disebutkan.|`filetype:"pdf"`|
|**link**|Mencari tautan eksternal yang mengarah ke suatu halaman.|`link:"kata kunci"`|
|**numrange**|Digunakan untuk menemukan angka atau rentang nilai spesifik.|`numrange:321-325`|
|**before / after**|Digunakan untuk mencari hasil dalam rentang tanggal tertentu.|`filetype:pdf & (before:2000-01-01 after:2001-01-01)`|
|**allinanchor** / **inanchor**|Menampilkan situs yang memiliki kata kunci pada teks tautan (anchor text) yang mengarah ke situs tersebut.|`inanchor:rat`|
|**allinpostauthor** / **inpostauthor**|Khusus untuk pencarian blog, digunakan untuk mencari artikel yang ditulis oleh penulis tertentu.|`allinpostauthor:"nama penulis"`|
|**related**|Menampilkan halaman web yang "mirip" dengan halaman web yang ditentukan.|`related:www.google.com`|
|**cache**|Menampilkan versi halaman web yang terakhir disimpan di dalam cache Google.|`cache:www.google.com`|

## Contoh Penggunaan

Plaintext

```
# Mencari direktori terbuka (open directory) yang memperlihatkan daftar file
intext:"index of /"

# Mencari file musik spesifik di direktori terbuka dan mengecualikan format web standar
Nina Simone intitle:”index.of” “parent directory” “size” “last modified” “description” I Put A Spell On You (mp4|mp3|avi|flac|aac|ape|ogg) -inurl:(jsp|php|html|aspx|htm|cf|shtml|lyrics-realm|mp3-collection) -site:.info

# Mencari file dokumen atau buku elektronik terkait kata kunci tertentu
Bill Gates intitle:”index.of” “parent directory” “size” “last modified” “description” Microsoft (pdf|txt|epub|doc|docx) -inurl:(jsp|php|html|aspx|htm|cf|shtml|ebooks|ebook) -site:.info

# Mencari folder utama (parent directory) untuk kategori video atau musik tanpa menyertakan ekstensi web
parent directory DVDRip -xxx -html -htm -php -shtml -opendivx -md5 -md5sums
parent directory MP3 -xxx -html -htm -php -shtml -opendivx -md5 -md5sums
parent directory [Nama Penyanyi atau Album] -xxx -html -htm -php -shtml -opendivx -md5 -md5sums

# Mencari file konfigurasi atau file web.config di server FTP
filetype:config inurl:web.config inurl:ftp

# Contoh pencarian kode registrasi atau serial lama (contoh: Windows XP)
“Windows XP Professional” 94FBR

# Mencari dokumen sensitif (gaji atau anggaran) dalam berbagai format dokumen
ext:(doc | pdf | xls | txt | ps | rtf | odt | sxw | psw | ppt | pps | xml) (intext:confidential salary | intext:"budget approved") inurl:confidential
```

## Operator Pencarian

#### Tanda Kutip Dua (`""`)

Mencari frasa yang **persis sama** di dalam tanda kutip. Sangat cocok jika kata kunci yang kamu gunakan ambigu atau ingin hasil yang benar-benar akurat.

Plaintext

```
"Tinned Sandwiches"
```

#### OR (`|`)

Operator ini digunakan untuk mencari istilah pertama **ATAU** istilah alternatif lainnya.

Plaintext

```
site:facebook.com | site:twitter.com
```

#### AND (`&`)

Digunakan untuk memastikan kedua kondisi atau kata kunci tersebut **harus ada** dalam hasil pencarian.

Plaintext

```
site:facebook.com & site:twitter.com
```

#### Kombinasi Operator

Kamu bisa menggabungkan beberapa operator menggunakan tanda kurung untuk membuat pencarian yang lebih kompleks.

Plaintext

```
(site:facebook.com | site:twitter.com) & intext:"login"
(site:facebook.com | site:twitter.com) (intext:"login")
```

#### Menyertakan Hasil (`+`)

Mengurutkan atau memastikan hasil pencarian lebih berfokus pada jumlah kemunculan kata kunci tersebut.

Plaintext

```
-site:facebook.com +site:facebook.*
```

#### Mengecualikan Hasil (`-`)

Digunakan untuk membuang atau **mengecualikan** kata, situs, atau ekstensi tertentu dari hasil pencarian.

Plaintext

```
site:facebook.* -site:facebook.com
```

#### Sinonim (`~`)

Menambahkan tanda tilde (`~`) di depan kata memberi tahu Google bahwa kamu juga ingin mencari **sinonim** dari kata tersebut.

> _Fakta seru: Kata "set" dalam bahasa Inggris memiliki definisi paling banyak di kamus._

Plaintext

```
~set
```

#### Pola Glob / Karakter Pengganti (`*`)

Tanda bintang (`*`) berfungsi sebagai _wildcard_ (isi apa saja). Sangat berguna untuk mencari lirik lagu yang setengah lupa atau nama domain dengan ekstensi apa pun.

Plaintext

```
site:*.com
```

- [Code](./index.md)

[Previously](info/pasive/00Shodan.md) | [Next](info/pasive/02Netcraft.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
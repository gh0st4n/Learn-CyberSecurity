# Script Python

Script ini menggunakan `googlesearch-python` library untuk melakukan pencarian dork secara otomatis.

## Script
[dork.py](dork.py)

## Cara Menggunakan Script

**1. Install dependensi:**
```bash
pip install googlesearch-python
```

**2. Lihat daftar kategori:**
```bash
python dork.py -l
```

**3. Cari semua kategori untuk target:**
```bash
python dork.py -t example.com
```

**4. Cari kategori tertentu:**
```bash
python dork.py -t example.com -c config_files
```

**5. Atur jumlah hasil dan delay:**
```bash
python dork.py -t example.com -c admin_panel -m 5 -d 3
```

**6. Simpan hasil ke file:**
```bash
python dork.py -t example.com > hasil_google_dork.txt
```

[Previously](info/pasive/00Shodan.md) | [Next](info/pasive/02Netcraft.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
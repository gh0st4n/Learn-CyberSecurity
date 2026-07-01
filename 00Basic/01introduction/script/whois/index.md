# Script Python

Berikut script Python untuk melakukan query whois dengan dua pendekatan: menggunakan library `whois` built-in dan raw socket manual.

## Script Pure Socket
[whois.py](whois.py)

## Script with Lib python-whois
[python-whois.py](python-whois.py)

## Usage
```
# Script 1 (pure socket)
python3 whois.py google.com

# Script 2 (library python-whois)
pip install python-whois
python3 python-whois.py google.com
python3 python-whois.py google.com --json
```

[Previously](../../info/pasive/02Netcraft.md) | [Next](../../info/active/01Dirb.md)

---

<div align="center">

[@T4n-Labs](https://t4n-labs.github.io/site) · [@Gh0sT4n](https://gh0st4n.github.io/site)

</div>
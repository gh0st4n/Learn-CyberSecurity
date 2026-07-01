#!/usr/bin/env python3
"""
Advanced Whois Tool - Using python-whois library
Install: pip install python-whois
"""

import whois
import json
import sys
from datetime import datetime

def query_whois(domain):
    """Query whois menggunakan library python-whois."""
    try:
        w = whois.whois(domain)
        return w
    except Exception as e:
        print(f"[!] Error querying {domain}: {e}")
        return None

def display_results(w, domain):
    """Tampilkan hasil query dalam format terstruktur."""
    print(f"\n{'='*60}")
    print(f" Whois Report: {domain}")
    print(f" Query Time  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    if w is None:
        return

    # Informasi umum
    print("[+] Domain Information")
    print(f"  Domain Name      : {w.domain_name or 'N/A'}")
    print(f"  Registrar        : {w.registrar or 'N/A'}")
    print(f"  Whois Server     : {w.whois_server or 'N/A'}")
    print(f"  DNSSEC           : {w.dnssec or 'N/A'}")

    # Tanggal
    print(f"\n[+] Important Dates")
    print(f"  Creation Date    : {w.creation_date or 'N/A'}")
    print(f"  Expiration Date  : {w.expiration_date or 'N/A'}")
    print(f"  Updated Date     : {w.updated_date or 'N/A'}")

    # Name Server
    print(f"\n[+] Name Servers")
    ns = w.name_servers or ['N/A']
    for i, n in enumerate(ns, 1):
        print(f"  NS{i}: {n}")

    # Status
    print(f"\n[+] Domain Status")
    status = w.status or ['N/A']
    for s in status:
        print(f"  • {s}")

    # Kontak
    print(f"\n[+] Registrant Info")
    print(f"  Name            : {w.name or 'N/A'}")
    print(f"  Organization    : {w.org or 'N/A'}")
    print(f"  Address         : {w.address or 'N/A'}")
    print(f"  City            : {w.city or 'N/A'}")
    print(f"  State           : {w.state or 'N/A'}")
    print(f"  Zip Code        : {w.zipcode or 'N/A'}")
    print(f"  Country         : {w.country or 'N/A'}")
    print(f"  Email           : {w.emails or 'N/A'}")

    # Admin & Tech
    for role in ['admin', 'tech']:
        key = f'{role}_'
        data = {k.replace(key, ''): v for k, v in w.items() if k.startswith(key)}
        if any(data.values()):
            print(f"\n[+] {role.capitalize()} Contact")
            print(f"  Name   : {data.get('name', 'N/A')}")
            print(f"  Email  : {data.get('email', 'N/A')}")
            print(f"  Phone  : {data.get('phone', 'N/A')}")

def export_json(w, filename=None):
    """Export hasil ke JSON."""
    if filename is None:
        filename = f"whois_{w.domain_name[0] if w.domain_name else 'unknown'}.json"

    # Convert datetime objects to string
    data = {}
    for k, v in w.items():
        if isinstance(v, list):
            data[k] = [str(x) if isinstance(x, datetime) else x for x in v]
        elif isinstance(v, datetime):
            data[k] = str(v)
        else:
            data[k] = v

    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\n[*] Results exported to: {filename}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 whois_advanced.py <domain> [--json]")
        print("Example: python3 whois_advanced.py google.com")
        print("         python3 whois_advanced.py google.com --json")
        sys.exit(1)

    domain = sys.argv[1]
    export_json_flag = '--json' in sys.argv

    w = query_whois(domain)
    if w:
        display_results(w, domain)
        if export_json_flag:
            export_json(w)

if __name__ == "__main__":
    main()

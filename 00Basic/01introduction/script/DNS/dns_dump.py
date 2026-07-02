#!/usr/bin/env python3
# dns_dump.py — script sederhana


import dns.resolver
import dns.zone
import dns.query
import sys

domain = sys.argv[1]
ns = sys.argv[2] if len(sys.argv) > 2 else None

# 1. Basic records
for qtype in ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']:
    try:
        answers = dns.resolver.resolve(domain, qtype)
        for rdata in answers:
            print(f"[{qtype}] {domain} -> {rdata}")
    except:
        pass

# 2. Zone transfer
if ns:
    try:
        z = dns.zone.from_xfr(dns.query.xfr(ns, domain))
        for name, node in z.nodes.items():
            print(f"[ZONE] {str(name)}.{domain}")
    except Exception as e:
        print(f"[!] AXFR failed: {e}")
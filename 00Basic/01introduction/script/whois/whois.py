#!/usr/bin/env python3
"""
Simple Whois Query Tool - Pure Python (no external deps)
Author: Gh0sT4n
Usage: python3 whois_tool.py example.com [whois_server]
"""

import socket
import sys

def whois_lookup(domain, server=None, port=43):
    """
    Melakukan query whois ke server yang sesuai.
    Jika server tidak ditentukan, akan mencoba mendeteksi berdasarkan TLD.
    """
    # Deteksi server whois berdasarkan TLD (sederhana)
    tld_servers = {
        'com': 'whois.verisign-grs.com',
        'net': 'whois.verisign-grs.com',
        'org': 'whois.pir.org',
        'id': 'whois.id',
        'io': 'whois.nic.io',
        'xyz': 'whois.nic.xyz',
    }

    if server is None:
        tld = domain.rsplit('.', 1)[-1].lower()
        server = tld_servers.get(tld, 'whois.iana.org')
        print(f"[*] Detected whois server for .{tld}: {server}")

    try:
        # Buat koneksi TCP ke server whois
        print(f"[*] Connecting to {server}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect((server, port))

        # Kirim query domain + newline
        query = f"{domain}\r\n"
        sock.sendall(query.encode())

        # Baca response
        response = b""
        while True:
            data = sock.recv(4096)
            if not data:
                break
            response += data

        sock.close()
        return response.decode('utf-8', errors='ignore')

    except socket.timeout:
        return "[!] Error: Connection timed out"
    except socket.gaierror:
        return f"[!] Error: Cannot resolve server {server}"
    except Exception as e:
        return f"[!] Error: {e}"

def parse_whois(raw):
    """Parse dan ekstrak informasi penting dari output whois."""
    important_fields = [
        'Domain Name', 'Registry Domain ID', 'Registrar',
        'Creation Date', 'Registry Expiry Date', 'Updated Date',
        'Name Server', 'Registrant Name', 'Registrant Organization',
        'Registrant Email', 'Admin Email', 'Tech Email',
        'DNSSEC', 'Domain Status'
    ]

    lines = raw.split('\n')
    parsed = {}
    for line in lines:
        for field in important_fields:
            if line.lower().startswith(field.lower()):
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    if key not in parsed:
                        parsed[key] = []
                    parsed[key].append(value)

    return parsed

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 whois_tool.py <domain> [whois_server]")
        print("Example: python3 whois_tool.py example.com")
        print("         python3 whois_tool.py example.com whois.verisign-grs.com")
        sys.exit(1)

    domain = sys.argv[1]
    server = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"\n{'='*60}")
    print(f" Whois Lookup: {domain}")
    print(f"{'='*60}\n")

    raw_result = whois_lookup(domain, server)

    # Tampilkan hasil lengkap
    print("[*] RAW WHOIS OUTPUT:")
    print("-" * 60)
    print(raw_result)
    print("-" * 60)

    # Parse dan tampilkan ringkasan
    parsed = parse_whois(raw_result)
    if parsed:
        print("\n[*] SUMMARY (Parsed Fields):")
        for key, values in parsed.items():
            for val in values:
                print(f"  {key:35s}: {val}")

if __name__ == "__main__":
    main()

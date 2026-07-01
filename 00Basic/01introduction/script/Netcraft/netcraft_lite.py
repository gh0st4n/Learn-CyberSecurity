#!/usr/bin/env python3
"""
NetCraft-Lite v1.0 - Website Recon & Fingerprinting Tool
OSINT passive recon: deteksi teknologi, server, SSL, DNS
"""

import sys
import ssl
import socket
import json
from datetime import datetime
from urllib.parse import urlparse

import requests
import dns.resolver
from bs4 import BeautifulSoup
from OpenSSL import crypto

# ============================================================
# KONFIGURASI
# ============================================================
TIMEOUT = 10
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
HEADERS = {"User-Agent": USER_AGENT}

# Teknologi fingerprints — regex-based detection
TECH_FINGERPRINTS = {
    "PHP": {
        "headers": {"X-Powered-By": r"PHP"},
        "cookies": [],
        "body": [],
        "url_extensions": [".php"],
    },
    "ASP.NET": {
        "headers": {"X-Powered-By": r"ASP\.NET", "X-AspNet-Version": r".*"},
        "cookies": ["ASP.NET_SessionId"],
        "body": [],
        "url_extensions": [".aspx", ".ashx", ".asmx"],
    },
    "Java/Spring": {
        "headers": {"X-Application-Context": r".*"},
        "cookies": ["JSESSIONID"],
        "body": [],
        "url_extensions": [".jsp", ".do"],
    },
    "Node.js/Express": {
        "headers": {"X-Powered-By": r"Express"},
        "cookies": ["connect.sid"],
        "body": [],
        "url_extensions": [],
    },
    "Python/Django": {
        "headers": {"X-Frame-Options": r".*"},
        "cookies": ["csrftoken", "sessionid"],
        "body": [],
        "url_extensions": [],
    },
    "Python/Flask": {
        "headers": {},
        "cookies": ["session"],
        "body": [],
        "url_extensions": [],
    },
    "Ruby on Rails": {
        "headers": {"X-Powered-By": r"Phusion|Ruby|Rails"},
        "cookies": ["_session_id"],
        "body": [],
        "url_extensions": [],
    },
    "WordPress": {
        "headers": {},
        "cookies": ["wordpress_", "wp-"],
        "body": [
            r"\/wp-content\/",
            r"\/wp-includes\/",
            r"\/wp-admin\/",
            r"\/wp-json\/",
            r"generator\">WordPress",
        ],
        "url_extensions": [],
    },
    "Joomla": {
        "headers": {},
        "cookies": [],
        "body": [r"\/media\/jui\/", r"joomla!", r"com_content"],
        "url_extensions": [],
    },
    "Drupal": {
        "headers": {},
        "cookies": ["Drupal"],
        "body": [r"Drupal", r"\/sites\/default\/", r"drupal\.js"],
        "url_extensions": [],
    },
    "Cloudflare": {
        "headers": {"Server": r"cloudflare", "CF-RAY": r".*"},
        "cookies": ["__cfduid", "__cf_bm"],
        "body": [],
        "url_extensions": [],
    },
    "Nginx": {
        "headers": {"Server": r"nginx"},
        "cookies": [],
        "body": [],
        "url_extensions": [],
    },
    "Apache": {
        "headers": {"Server": r"Apache"},
        "cookies": [],
        "body": [],
        "url_extensions": [],
    },
    "IIS": {
        "headers": {"Server": r"Microsoft-IIS"},
        "cookies": [],
        "body": [],
        "url_extensions": [".asp"],
    },
    "LiteSpeed": {
        "headers": {"Server": r"LiteSpeed"},
        "cookies": [],
        "body": [],
        "url_extensions": [],
    },
    "Caddy": {
        "headers": {"Server": r"Caddy"},
        "cookies": [],
        "body": [],
        "url_extensions": [],
    },
    "OpenResty": {
        "headers": {"Server": r"openresty"},
        "cookies": [],
        "body": [],
        "url_extensions": [],
    },
    "Varnish": {
        "headers": {"Via": r".*varnish", "X-Varnish": r".*"},
        "cookies": [],
        "body": [],
        "url_extensions": [],
    },
    "React": {
        "headers": {},
        "cookies": [],
        "body": [
            r"__NEXT_DATA__",
            r"react\.js",
            r"react-dom",
            r"root\">",
            r"_next\/static",
            r"create-react-app",
        ],
        "url_extensions": [],
    },
    "Vue.js": {
        "headers": {},
        "cookies": [],
        "body": [r"vue\.js", r"vue\.min\.js", r"__vue__", r"data-v-"],
        "url_extensions": [],
    },
    "Angular": {
        "headers": {},
        "cookies": [],
        "body": [r"angular\.js", r"angular\.min\.js", r"ng-app", r"ng-"],
        "url_extensions": [],
    },
    "Google Analytics": {
        "headers": {},
        "cookies": ["_ga", "_gid", "_gat"],
        "body": [r"google-analytics\.com\/analytics\.js", r"gtag\("],
        "url_extensions": [],
    },
}

# ============================================================
# WARNA OUTPUT — biar keren
# ============================================================
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_banner():
    banner = f"""
    {CYAN}{BOLD}
    ╔═══════════════════════════════════════════╗
    ║       NetCraft-Lite — Website Recon        ║
    ║       OSINT Passive Fingerprinting Tool    ║
    ╚═══════════════════════════════════════════╝{RESET}
    """
    print(banner)


# ============================================================
# DNS ENUMERATION
# ============================================================
def dns_enumeration(domain):
    """Lakukan DNS lookup untuk berbagai record type."""
    print(f"\n{GREEN}[+] DNS Enumeration untuk: {domain}{RESET}")

    records = {
        "A": "IPv4 Address",
        "AAAA": "IPv6 Address",
        "MX": "Mail Servers",
        "NS": "Nameservers",
        "TXT": "TXT Records",
        "SOA": "Start of Authority",
        "CNAME": "Canonical Name",
    }

    for record_type, description in records.items():
        try:
            resolver = dns.resolver.Resolver()
            resolver.timeout = TIMEOUT
            resolver.lifetime = TIMEOUT
            answers = resolver.resolve(domain, record_type)
            
            print(f"\n  {YELLOW}{description}:{RESET}")
            for rdata in answers:
                print(f"    → {rdata}")
                
        except dns.resolver.NoAnswer:
            pass
        except dns.resolver.NXDOMAIN:
            print(f"\n  {RED}[!] Domain tidak ditemukan.{RESET}")
            return
        except dns.resolver.LifetimeTimeout:
            print(f"\n  {YELLOW}  [!] Timeout untuk {record_type}{RESET}")
        except Exception as e:
            print(f"\n  {RED}  [!] Error {record_type}: {e}{RESET}")


# ============================================================
# HTTP HEADER & TECHNOLOGY FINGERPRINTING
# ============================================================
def fetch_headers(url):
    """Fetch HTTP response headers."""
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False, allow_redirects=True)
        return resp
    except requests.exceptions.ConnectionError:
        # Coba HTTPS dulu, fallback ke HTTP
        if url.startswith("https://"):
            http_url = url.replace("https://", "http://")
            try:
                resp = requests.get(http_url, headers=HEADERS, timeout=TIMEOUT, verify=False, allow_redirects=True)
                return resp
            except:
                return None
    except Exception:
        return None


def fingerprint_technologies(response, url):
    """Deteksi teknologi dari headers, cookies, dan body."""
    detected = []
    
    if response is None:
        return detected

    headers = response.headers
    cookies = response.cookies
    body = response.text.lower()
    parsed = urlparse(url)
    path = parsed.path.lower()

    for tech_name, patterns in TECH_FINGERPRINTS.items():
        score = 0
        reasons = []

        # Cek headers
        for header, pattern in patterns["headers"].items():
            if header in headers:
                import re
                if re.search(pattern, headers[header], re.IGNORECASE):
                    score += 2
                    reasons.append(f"Header {header}: {headers[header]}")

        # Cek cookies
        for cookie_pattern in patterns["cookies"]:
            for cookie in cookies:
                if cookie_pattern.lower() in cookie.name.lower():
                    score += 1
                    reasons.append(f"Cookie: {cookie.name}")
                    break

        # Cek body
        for body_pattern in patterns["body"]:
            if re.search(body_pattern, body, re.IGNORECASE):
                score += 1
                reasons.append("Body match")

        # Cek URL extension
        for ext in patterns["url_extensions"]:
            if path.endswith(ext):
                score += 1
                reasons.append(f"URL extension: {ext}")

        if score >= 2:
            detected.append({
                "technology": tech_name,
                "confidence": min(100, score * 20),
                "reasons": reasons[:3],
            })

    return detected


def display_headers(response):
    """Tampilkan header HTTP yang informatif."""
    if response is None:
        return

    print(f"\n{GREEN}[+] HTTP Response Headers:{RESET}")
    interesting_headers = [
        "Server", "X-Powered-By", "X-AspNet-Version", "X-AspNetMvc-Version",
        "X-Generator", "X-Drupal-Cache", "X-Varnish", "CF-RAY",
        "X-Cache", "X-Cache-Hits", "Age", "Via", "X-Backend-Server",
        "X-Served-By", "X-Pingback", "Link", "X-Frame-Options",
        "Content-Security-Policy", "Strict-Transport-Security",
        "Set-Cookie", "X-Content-Type-Options", "X-XSS-Protection",
        "Access-Control-Allow-Origin",
    ]

    for header in interesting_headers:
        if header in response.headers:
            value = response.headers[header]
            if any(x in header.lower() for x in ["powered", "generator", "version", "server"]):
                print(f"  {YELLOW}{header}:{RESET} {GREEN}{value}{RESET}")
            else:
                print(f"  {YELLOW}{header}:{RESET} {value}")

    print(f"\n  {YELLOW}Status Code:{RESET} {response.status_code}")
    print(f"  {YELLOW}Content-Type:{RESET} {response.headers.get('Content-Type', 'N/A')}")
    print(f"  {YELLOW}Content-Length:{RESET} {response.headers.get('Content-Length', 'N/A')}")
    print(f"  {YELLOW}Redirect History:{RESET} {' → '.join([str(r.status_code) for r in response.history]) if response.history else 'None'}")


# ============================================================
# SSL/TLS CERTIFICATE ANALYSIS
# ============================================================
def analyze_ssl(hostname, port=443):
    """Analisis sertifikat SSL/TLS."""
    print(f"\n{GREEN}[+] SSL/TLS Certificate Analysis:{RESET}")
    
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        with socket.create_connection((hostname, port), timeout=TIMEOUT) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert_bin = ssock.getpeercert(binary_form=True)
                cert = crypto.load_certificate(crypto.FILETYPE_ASN1, cert_bin)

                # Subject
                subject = dict(cert.get_subject().get_components())
                print(f"  {YELLOW}Common Name (CN):{RESET} {subject.get(b'CN', b'N/A').decode()}")

                # Issuer
                issuer = dict(cert.get_issuer().get_components())
                print(f"  {YELLOW}Issuer:{RESET} {issuer.get(b'CN', b'N/A').decode()}")

                # Validity
                not_before = datetime.strptime(cert.get_notBefore().decode(), "%Y%m%d%H%M%SZ")
                not_after = datetime.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ")
                print(f"  {YELLOW}Valid From:{RESET} {not_before}")
                print(f"  {YELLOW}Valid Until:{RESET} {not_after}")
                
                days_left = (not_after - datetime.now()).days
                if days_left < 30:
                    print(f"  {RED}  ⚠ Expiring in {days_left} days!{RESET}")
                else:
                    print(f"  {GREEN}  ✓ Valid for {days_left} days{RESET}")

                # SAN (Subject Alternative Names) — CRUCIAL untuk subdomain
                san = []
                for i in range(cert.get_extension_count()):
                    ext = cert.get_extension(i)
                    if ext.get_short_name() == b"subjectAltName":
                        san_str = str(ext)
                        san = [s.strip() for s in san_str.replace("DNS:", "").split(",")]

                if san:
                    print(f"\n  {YELLOW}Subject Alternative Names (SAN):{RESET}")
                    for name in san:
                        print(f"    → {GREEN}{name}{RESET}")

                # SSL/TLS Version & Cipher
                print(f"\n  {YELLOW}SSL/TLS Version:{RESET} {ssock.version()}")
                print(f"  {YELLOW}Cipher:{RESET} {ssock.cipher()}")

    except socket.timeout:
        print(f"  {RED}[!] Connection timeout{RESET}")
    except ConnectionRefusedError:
        print(f"  {YELLOW}[!] Koneksi ditolak (port {port} tidak terbuka){RESET}")
    except Exception as e:
        print(f"  {RED}[!] SSL Error: {e}{RESET}")


# ============================================================
# WHOIS / IP LOOKUP (via hackertarget.com — free API)
# ============================================================
def ip_info(domain):
    """Dapatkan IP address domain."""
    try:
        ip = socket.gethostbyname(domain)
        print(f"\n{GREEN}[+] IP Address:{RESET} {CYAN}{ip}{RESET}")
        return ip
    except socket.gaierror:
        print(f"\n{RED}[!] Gagal resolve IP{RESET}")
        return None


# ============================================================
# MAIN RECON FUNCTION
# ============================================================
def recon(url):
    """Main reconnaissance function."""
    print_banner()
    
    # Parse URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    
    parsed = urlparse(url)
    domain = parsed.netloc
    hostname = domain.split(":")[0]

    print(f"{BOLD}Target: {CYAN}{url}{RESET}")
    print(f"{BOLD}Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print("=" * 55)

    # 1. DNS Enumeration
    dns_enumeration(hostname)

    # 2. IP Info
    ip = ip_info(hostname)

    # 3. HTTP Headers & Technology Detection
    print(f"\n{GREEN}[+] Fetching HTTP Headers...{RESET}")
    response = fetch_headers(url)
    display_headers(response)

    # 4. Technology Fingerprinting
    print(f"\n{GREEN}[+] Detected Technologies:{RESET}")
    technologies = fingerprint_technologies(response, url)
    if technologies:
        for tech in technologies:
            level = GREEN if tech["confidence"] >= 60 else YELLOW
            print(f"  {level}✓ {tech['technology']} (confidence: {tech['confidence']}%){RESET}")
            for reason in tech["reasons"]:
                print(f"    └─ {reason}")
    else:
        print(f"  {YELLOW}[!] Tidak ada teknologi yang terdeteksi{RESET}")

    # 5. SSL/TLS Analysis (hanya jika HTTPS)
    if url.startswith("https://"):
        analyze_ssl(hostname, 443)

    # Summary
    print(f"\n{'=' * 55}")
    print(f"{BOLD}Recon selesai. Target: {CYAN}{domain}{RESET}")
    print(f"{BOLD}Selesai pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{'=' * 55}")


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if len(sys.argv) < 2:
        print(f"{BOLD}Usage:{RESET}")
        print(f"  python3 netcraft_lite.py <target.com>")
        print(f"  python3 netcraft_lite.py https://target.com/path")
        print(f"\n{BOLD}Examples:{RESET}")
        print(f"  python3 netcraft_lite.py example.com")
        print(f"  python3 netcraft_lite.py https://google.com")
        sys.exit(1)

    target = sys.argv[1]
    recon(target)
#!/usr/bin/env python3
"""
SimpleDirb - Web Content Scanner (Dirb-like)
Simple directory/file brute-force tool untuk educational purpose
"""

import requests
import sys
import threading
from queue import Queue
from urllib.parse import urljoin

# Konfigurasi
THREAD_COUNT = 10
TIMEOUT = 5
USER_AGENT = "HackerAI-SimpleDirb/1.0"

# Warna terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Queue untuk thread
queue = Queue()
found_items = []
lock = threading.Lock()

def banner():
    print(f"""
{BLUE}╔══════════════════════════════════╗
║       SimpleDirb v1.0               ║
║  Web Content Scanner (Dirb-like)    ║
║      HackerAI Educational Tool      ║
╚══════════════════════════════════╝{RESET}
    """)

def scan_directory(base_url, word, extensions=None):
    """Scan satu direktori/file"""
    results = []
    
    # Coba tanpa ekstensi
    url = urljoin(base_url, word)
    results.append((url, None))
    
    # Coba dengan ekstensi
    if extensions:
        for ext in extensions:
            ext = ext.strip().lstrip(".")
            url_ext = url.rstrip("/") + f".{ext}"
            results.append((url_ext, ext))
    
    return results

def check_url(url):
    """Kirim HTTP request dan analisis response"""
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=TIMEOUT, allow_redirects=False)
        status = response.status_code
        
        if status == 200:
            return (GREEN, f"FOUND     ({status})")
        elif status in [301, 302, 307, 308]:
            return (YELLOW, f"REDIRECT  ({status}) → {response.headers.get('Location', 'N/A')}")
        elif status == 401:
            return (YELLOW, f"AUTH REQ  ({status})")
        elif status == 403:
            return (RED, f"FORBIDDEN ({status})")
        elif status == 500:
            return (RED, f"ERROR     ({status})")
        elif status in [404]:
            return None  # Not found, skip
        else:
            return (BLUE, f"CODE      ({status})")
            
    except requests.exceptions.RequestException:
        return None

def worker(base_url, extensions, verbose=False):
    """Worker thread"""
    while not queue.empty():
        word = queue.get()
        urls_to_check = scan_directory(base_url, word, extensions)
        
        for url, ext in urls_to_check:
            result = check_url(url)
            if result:
                color, status_text = result
                with lock:
                    line = f"  [{status_text}]  {url}"
                    print(f"{color}{line}{RESET}")
                    found_items.append((url, ext, status_text))
            elif verbose:
                with lock:
                    pass  # Silent mode by default
        
        queue.task_done()

def main():
    banner()
    
    # Parsing argumen
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <url> [wordlist] [options]")
        print(f"       {sys.argv[0]} http://target.com/")
        print(f"       {sys.argv[0]} http://target.com/ /path/to/wordlist.txt -X php,html")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip("/") + "/"
    wordlist_path = sys.argv[2] if len(sys.argv) > 2 else "/usr/share/wordlists/dirb/common.txt"
    
    # Parse extensions
    extensions = None
    if "-X" in sys.argv:
        idx = sys.argv.index("-X")
        if idx + 1 < len(sys.argv):
            extensions = sys.argv[idx + 1].split(",")
    
    # Parse thread count
    global THREAD_COUNT
    if "-t" in sys.argv:
        idx = sys.argv.index("-t")
        if idx + 1 < len(sys.argv):
            THREAD_COUNT = int(sys.argv[idx + 1])
    
    # Parse output file
    output_file = None
    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            output_file = sys.argv[idx + 1]
    
    print(f"{BLUE}[+] Target:{RESET}       {base_url}")
    print(f"{BLUE}[+] Wordlist:{RESET}     {wordlist_path}")
    print(f"{BLUE}[+] Extensions:{RESET}   {extensions if extensions else 'None'}")
    print(f"{BLUE}[+] Threads:{RESET}      {THREAD_COUNT}")
    print()
    
    # Load wordlist
    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            words = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        print(f"{RED}[!] Wordlist tidak ditemukan: {wordlist_path}{RESET}")
        sys.exit(1)
    
    print(f"{BLUE}[+] Loaded {len(words)} words{RESET}")
    print(f"{YELLOW}[*] Scanning...{RESET}\n")
    
    # Masukkan ke queue
    for word in words:
        queue.put(word)
    
    # Jalankan thread
    threads = []
    for _ in range(min(THREAD_COUNT, len(words))):
        t = threading.Thread(target=worker, args=(base_url, extensions))
        t.daemon = True
        t.start()
        threads.append(t)
    
    # Tunggu selesai
    for t in threads:
        t.join()
    
    queue.join()
    
    # Summary
    print(f"\n{GREEN}[+] Scan selesai!{RESET}")
    print(f"{GREEN}[+] Ditemukan: {len(found_items)} item{RESET}")
    
    if found_items:
        print(f"\n{BLUE}=== SUMMARY ==={RESET}")
        for url, ext, status in found_items:
            print(f"  {url}")
    
    # Simpan ke file jika diminta
    if output_file:
        with open(output_file, "w") as f:
            f.write(f"SimpleDirb Scan Results\n")
            f.write(f"Target: {base_url}\n")
            f.write(f"Wordlist: {wordlist_path}\n")
            f.write(f"Found: {len(found_items)} items\n\n")
            for url, ext, status in found_items:
                f.write(f"{url}\n")
        print(f"\n{GREEN}[+] Hasil disimpan ke: {output_file}{RESET}")

if __name__ == "__main__":
    main()
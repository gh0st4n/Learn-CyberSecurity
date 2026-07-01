#!/usr/bin/env python3
"""
Google Dork Tool - Sederhana
Penjelasan: Script untuk membantu pencarian Google Dorking
Author: Gh0sT4n
"""

import sys
import time
import argparse
from datetime import datetime

try:
    from googlesearch import search
except ImportError:
    print("[!] Library 'googlesearch-python' belum terinstall.")
    print("[*] Install dengan: pip install googlesearch-python")
    sys.exit(1)


# Database Dork Sederhana
DORK_DATABASE = {
    "dir_listing": {
        "description": "Mencari direktori dengan listing terbuka",
        "dorks": [
            'intitle:"index of" {target}',
            'intitle:"index of /" "parent directory" {target}',
            'intitle:"index of" "backup" {target}',
        ]
    },
    "config_files": {
        "description": "Mencari file konfigurasi sensitif",
        "dorks": [
            'filetype:env "DB_PASSWORD" {target}',
            'filetype:conf "mysql" "password" {target}',
            'filetype:ini "mysql" "password" {target}',
            'filetype:cfg "password" {target}',
        ]
    },
    "database": {
        "description": "Mencari dump database dan file SQL",
        "dorks": [
            'filetype:sql "INSERT INTO" "password" {target}',
            'filetype:sql "MySQL dump" {target}',
            'filetype:sql "CREATE TABLE" {target}',
        ]
    },
    "log_files": {
        "description": "Mencari file log yang terekspos",
        "dorks": [
            'filetype:log "password" {target}',
            'filetype:log "username" {target}',
            'filetype:log "error" "PHP" {target}',
        ]
    },
    "backup_files": {
        "description": "Mencari file backup",
        "dorks": [
            'filetype:bak site:{target}',
            'filetype:old site:{target}',
            'filetype:swp site:{target}',
            'inurl:backup filetype:zip {target}',
        ]
    },
    "admin_panel": {
        "description": "Mencari panel admin/login",
        "dorks": [
            'inurl:admin intitle:login {target}',
            'inurl:administrator {target}',
            'inurl:wp-admin {target}',
            'inurl:/manager {target}',
        ]
    },
    "exposed_docs": {
        "description": "Mencari dokumen sensitif",
        "dorks": [
            'filetype:xls "email" "password" {target}',
            'filetype:pdf "confidential" {target}',
            'filetype:docx "password" {target}',
            'filetype:csv "username" "password" {target}',
        ]
    },
    "all": {
        "description": "Menjalankan SEMUA kategori dork",
        "dorks": []  # Khusus, akan di-handle terpisah
    }
}


def banner():
    """Menampilkan banner tool"""
    print("=" * 60)
    print("  Google Dork Tool v1.0")
    print("  Untuk tujuan pengujian keamanan yang sah")
    print(f"  Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


def search_dork(dork_query, max_results=10, delay=2):
    """
    Melakukan pencarian Google dengan query dork.
    
    Args:
        dork_query (str): Query Google Dork
        max_results (int): Jumlah maksimal hasil
        delay (int): Jeda antar request (detik)
    
    Returns:
        list: Daftar URL hasil pencarian
    """
    results = []
    try:
        print(f"    [*] Mencari: {dork_query}")
        for url in search(dork_query, num_results=max_results):
            results.append(url)
            print(f"       -> {url}")
        time.sleep(delay)  # Jeda agar tidak kena rate limit
    except Exception as e:
        print(f"    [!] Error: {e}")
    
    return results


def run_category(category_name, target, max_results, delay):
    """Menjalankan semua dork dalam satu kategori"""
    category = DORK_DATABASE.get(category_name)
    if not category:
        print(f"[!] Kategori '{category_name}' tidak ditemukan.")
        return []
    
    print(f"\n[+] Kategori: {category_name}")
    print(f"    Deskripsi: {category['description']}")
    
    all_results = []
    for dork_template in category["dorks"]:
        dork_query = dork_template.replace("{target}", target)
        results = search_dork(dork_query, max_results, delay)
        all_results.extend(results)
        print()  # Baris baru antar dork
    
    return all_results


def list_categories():
    """Menampilkan daftar kategori yang tersedia"""
    print("\n[*] Kategori Dork yang tersedia:")
    print("-" * 50)
    for key, value in DORK_DATABASE.items():
        if key != "all":
            print(f"  {key:20s} - {value['description']}")
    print("-" * 50)


def main():
    parser = argparse.ArgumentParser(
        description="Google Dork Tool - Pencarian informasi sensitif via Google",
        epilog="Contoh: python dork.py -t example.com -c config_files"
    )
    
    parser.add_argument("-t", "--target", help="Target domain (contoh: example.com)")
    parser.add_argument("-c", "--category", default="all",
                        help="Kategori dork (default: semua)")
    parser.add_argument("-m", "--max", type=int, default=10,
                        help="Maksimal hasil per dork (default: 10)")
    parser.add_argument("-d", "--delay", type=int, default=2,
                        help="Jeda antar request dalam detik (default: 2)")
    parser.add_argument("-l", "--list", action="store_true",
                        help="Tampilkan daftar kategori yang tersedia")
    
    args = parser.parse_args()
    
    banner()
    
    # Jika minta daftar kategori
    if args.list:
        list_categories()
        return
    
    # Validasi target
    if not args.target:
        print("\n[!] Target tidak boleh kosong.")
        print("[*] Gunakan -t untuk menentukan target.")
        print("[*] Contoh: python dork.py -t example.com -c config_files")
        list_categories()
        return
    
    print(f"\n[*] Target: {args.target}")
    print(f"[*] Maksimal hasil per dork: {args.max}")
    print(f"[*] Jeda antar request: {args.delay} detik")
    print(f"[*] Peringatan: Gunakan dengan bijak dan hanya pada target yang sah!\n")
    
    all_results = []
    
    if args.category == "all":
        # Jalankan semua kategori
        print("[*] Menjalankan SEMUA kategori...")
        for cat_name in DORK_DATABASE:
            if cat_name != "all":
                results = run_category(cat_name, args.target, args.max, args.delay)
                all_results.extend(results)
    else:
        # Jalankan kategori tertentu
        results = run_category(args.category, args.target, args.max, args.delay)
        all_results.extend(results)
    
    # Ringkasan akhir
    print("\n" + "=" * 60)
    print(f"[+] Selesai! Total URL ditemukan: {len(set(all_results))}")
    print("[+] Simpan hasil dengan redirect output:")
    print(f"    python {sys.argv[0]} -t {args.target} -c {args.category} > hasil_dork.txt")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import os
import sys
import time
import zlib
import logging
import string
import itertools
import zipfile
import bannerZip

from threading import Event
from colorama import Fore, Back, Style, init
from concurrent.futures import ThreadPoolExecutor, as_completed

init(autoreset=True)

# ===================================================================
# Loading Animasi Sederhana

def loading_animation(message):
    chars = "|/-\\"
    for i in range(20):  # Durasi animasi
        sys.stdout.write(f'\r{message} {chars[i % len(chars)]}')
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r')

# ===================================================================
# Setup Logging
logging.basicConfig(filename='zip_cracker.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Jumlah Thread Yang Digunakan
THREADS = 4
password_found = Event()  # Event untuk menandai password ditemukan
karakter = string.ascii_lowercase + string.digits

# ===================================================================
# Fungsi untuk mencoba membuka file ZIP dengan password
def ekstrak_zip(file_zip, password):
    try:
        file_zip.extractall(pwd=password.encode('UTF-8'))
        logging.info(f"Password Ditemukan ► {password}")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}\n[!] Password Ditemukan {Fore.LIGHTBLUE_EX}{Style.BRIGHT}► {Fore.LIGHTCYAN_EX}{Style.BRIGHT}{password}")
        return True
    except (RuntimeError, zipfile.BadZipFile, zlib.error) as e:
        logging.error(f"Error: {e}")
        return False

# ===================================================================
# Fungsi brute force tanpa wordlist (dengan kombinasi karakter)
def brute_force_worker(file_name, password_list):
    try:
        file_zip = zipfile.ZipFile(file_name)
        for password in password_list:
            if password_found.is_set():
                return None
            if ekstrak_zip(file_zip, password):
                password_found.set()
                return password
        return None
    except Exception as e:
        logging.error(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[!] {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}Error di Thread: {e}")
        return None

def brute_force_zip(file_name):
    try:
        file_zip = zipfile.ZipFile(file_name)
    except zipfile.BadZipFile:
        logging.error("File Zip Tidak Valid.")
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[!] {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}File Zip Tidak Valid.")
        return

    for panjang_password in range(1, 7):
        total_kombinasi = len(karakter) ** panjang_password
        logging.info(f"[+] Mulai mencoba password panjang {panjang_password} dengan {total_kombinasi} kombinasi.")
        print(f"\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] Mencoba Password Panjang {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{panjang_password} {Fore.LIGHTCYAN_EX}{Style.BRIGHT}({total_kombinasi} kombinasi)")

        mulai_waktu = time.time()

        with ThreadPoolExecutor(max_workers=THREADS) as executor:
            password_generator = itertools.product(karakter, repeat=panjang_password)
            futures = []

            for _ in range(THREADS):
                batch_password = [''.join(p) for p in itertools.islice(password_generator, total_kombinasi // THREADS)]
                futures.append(executor.submit(brute_force_worker, file_name, batch_password))

            while not password_found.is_set() and any(not future.done() for future in futures):
                loading_animation(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}Cracking Panjang Password {Fore.LIGHTGREEN_EX}{Style.BRIGHT}{panjang_password}")

            for future in as_completed(futures):
                result = future.result()
                if result:
                    print(f"\n\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}Password berhasil ditemukan {Fore.LIGHTBLUE_EX}{Style.BRIGHT}► {Fore.LIGHTCYAN_EX}{Style.BRIGHT}{result}")
                    break

        waktu_selesai = time.time()
        elapsed_time = waktu_selesai - mulai_waktu
        print(f"\n{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}[!] Proses Panjang Password {Fore.LIGHTGREEN_EX}{Style.BRIGHT}{panjang_password} {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}Selesai Dalam {Fore.LIGHTGREEN_EX}{Style.BRIGHT}{elapsed_time:.2f} detik")

        if password_found.is_set():
            break

# ===================================================================
# Fungsi brute force dengan wordlist
def brute_force_zip_with_wordlist(file_name, wordlist_file):
    try:
        file_zip = zipfile.ZipFile(file_name)
    except zipfile.BadZipFile:
        logging.error("File Zip Tidak Valid.")
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[!] {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}File Zip Tidak Valid.")
        return

    try:
        with open(wordlist_file, 'r') as f:
            for line in f:
                password = line.strip()
                print(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] Mencoba Password: {Fore.LIGHTYELLOW_EX}{password}")
                if ekstrak_zip(file_zip, password):
                    break
    except FileNotFoundError:
        print(f"Wordlist file '{wordlist_file}' tidak ditemukan.")
        logging.error(f"Wordlist file '{wordlist_file}' tidak ditemukan.")

# ===================================================================
# Fungsi Utama
def main():
    bannerZip.clear_screen()
    bannerZip.banner_me()

    print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[1] {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}Brute Force Tanpa Wordlist")
    print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}[2] {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}Brute Force Dengan Wordlist")

    choice = int(input(f"\n\n{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[ ZipLo ] {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}► {Fore.LIGHTRED_EX}{Style.BRIGHT}"))

    if choice == 1:
        bannerZip.clear_screen()
        bannerZip.banner_me()
        file_name = input(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}File Name {Fore.LIGHTBLUE_EX}{Style.BRIGHT}► {Fore.LIGHTRED_EX}{Style.BRIGHT}")
        print (f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}=========================================")
        brute_force_zip(file_name)
    elif choice == 2:
        bannerZip.clear_screen()
        bannerZip.banner_me()
        file_name = input(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}File Name {Fore.LIGHTBLUE_EX}{Style.BRIGHT}► {Fore.LIGHTRED_EX}{Style.BRIGHT}")
        wordlist_file = input(f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}[+] {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}Wordlist {Fore.LIGHTBLUE_EX}{Style.BRIGHT}► {Fore.LIGHTRED_EX}{Style.BRIGHT}")
        print (f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}=========================================")
        brute_force_zip_with_wordlist(file_name, wordlist_file)
    else:
        print("exit")

if __name__ == "__main__":
    main()

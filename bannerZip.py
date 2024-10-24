import os
import time

from colorama import Fore, Back, Style, init

init(autoreset=True)


def banner_me():
    abc = f"""
{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╔════════════════▣◎▣════════════════╗
███████╗██╗██████{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╗ ██╗      ██████╗
╚══███╔╝██║██╔══██{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╗██║     ██╔═══██╗
  ███╔╝ ██║██████{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╔╝██║     ██║   ██║
 ███╔╝  ██║██{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╔═══╝ ██║     ██║   ██║
███████╗██║██{Fore.LIGHTGREEN_EX}{Style.BRIGHT}║     ███████╗╚██████╔╝
{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╚══════╝╚═╝╚═╝     ╚══════╝ ╚═════╝
{Fore.LIGHTGREEN_EX}{Style.BRIGHT}╚════════════════▣◎▣════════════════╝

{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}           ZIP CRACKER

    """

    for banner in abc.split('\n'):
        time.sleep(0.1)
        print (banner)


def clear_screen():
    if os.name == 'posix':
        os.system("clear")
    else:
        os.system("cls")


if __name__ == '__main__':
    banner_me()

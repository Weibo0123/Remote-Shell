import pyfiglet
from colorama import Fore, init, Style
import sys
import time
import getpass

init(autoreset=True)

INFO = Fore.CYAN
SUCCESS = Fore.GREEN
WARNING = Fore.YELLOW
ERROR   = Fore.RED

def hacker_banner(text="Remote Shell", font="slant", delay=0.03):
    ascii_banner = pyfiglet.figlet_format(text, font=font)
    for line in ascii_banner.split("\n"):
        for char in line:
            sys.stdout.write(Fore.GREEN + char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def startup_sequence():
    loading(" Initializing Remote Shell...", 5)
    time.sleep(0.5)
    print(Fore.CYAN + "[*] Ready to connect to your targets!\n")
    time.sleep(0.5)

def printc(msg, color=INFO, end="\n"):
    print(color + msg + Style.RESET_ALL, end=end)

def print_info(msg):
    printc(f"msg", INFO)

def print_success(msg):
    printc(f"msg", SUCCESS)

def print_warning(msg):
    printc(f"msg", WARNING)

def print_error(msg):
    printc(f"msg", ERROR)

def prompt(text, color=Fore.CYAN):
    return color + text + Style.RESET_ALL

def get_pass(text, color=Fore.LIGHTMAGENTA_EX):
    return getpass.getpass(color + text + Style.RESET_ALL)

def loading(text="Connecting", duration=2):
    spinner = "|/-\\"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{INFO}[{spinner[i % len(spinner)]}] {text}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write("\r" + " " * 50 + "\r")
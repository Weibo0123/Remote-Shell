"""
hacker_banner.py

Provides hacker-style UI utilities:
ASCII banners
Colored output
Loading animations
"""
import pyfiglet
from colorama import Fore, init, Style
import sys
import time
import getpass

# Initialize colorama so colors reset automatically after each print
init(autoreset=True)

# Define commonly used colors for different message types
INFO = Fore.CYAN
SUCCESS = Fore.GREEN
WARNING = Fore.YELLOW
ERROR   = Fore.RED

def hacker_banner(text="Remote Shell", font="slant", delay=0.03):
    """
    Display an animated ASCII banner using pyfiglet.
    """
    ascii_banner = pyfiglet.figlet_format(text, font=font)
    # Print the banner line by line, character by character
    for line in ascii_banner.split("\n"):
        for char in line:
            sys.stdout.write(Fore.GREEN + char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def startup_sequence():
    """
    Display a startup loading animation and message.
    """
    loading(" Initializing Remote Shell...", 5)
    time.sleep(0.5)
    print(Fore.CYAN + "[*] Ready to connect to your targets!\n")
    time.sleep(0.5)

def printc(msg, color=INFO, end="\n"):
    """
    Base colored print function used by all other print helpers,
    """

    print(color + msg + Style.RESET_ALL, end=end)

def print_info(msg):
    """
    Print information message.
    """
    printc(f"{msg}", INFO)

def print_success(msg):
    """
    Print success message.
    """
    printc(f"{msg}", SUCCESS)

def print_warning(msg):
    """
    Print warning message.
    """
    printc(f"{msg}", WARNING)

def print_error(msg):
    """
    Print error message.
    """
    printc(f"{msg}", ERROR)

def prompt(text, color=Fore.CYAN):
    """
    Prompt user for input with color text.
    """
    return input(color + text + Style.RESET_ALL)

def get_pass(text, color=Fore.LIGHTMAGENTA_EX):
    """
    Prompt user for password with color text.
    """
    return getpass.getpass(color + text + Style.RESET_ALL)

def loading(text="Connecting", duration=2):
    """
    Display a loading animation.
    """
    spinner = "|/-\\"
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{INFO}[{spinner[i % len(spinner)]}] {text}...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1

    sys.stdout.write("\r" + " " * 50 + "\r")
import os
import json
import ipaddress
import sys
from hacker_banner import print_info, print_error, print_success, print_warning, prompt, get_pass, loading

# The target saving file
DATA_DIR = "data"
TARGET_SAVE_FILE = os.path.join(DATA_DIR, "targets.json")


def check_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def check_target(name, ip, port, user):
    if not (0 < len(name) <= 14):
        raise ValueError("Target name must be between 1 and 14 characters long")

    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise ValueError("Invalid IP address")

    try:
        port = int(port)
    except (TypeError, ValueError):
        raise ValueError("Invalid port number")
    if not (1 <= port <= 65535):
        raise ValueError("Port must be between 1 and 65535")

    if not user:
        raise ValueError("Username cannot be empty")

def save_target(name, ip, port, user):
    check_data_dir()
    targets = load_target() or {}

    if name in targets:
        confirm = prompt(f"Target {name} already exists. Overwrite? [y/n] ").lower()
        if confirm not in ["y", "yes"]:
            sys.exit("Saving cancelled")

    targets[name] = {
        "ip": ip,
        "port": port,
        "user": user,
    }

    with open(TARGET_SAVE_FILE, "w") as f:
        json.dump(targets, f, indent=4)

    print_success(f"Target '{name}' successfully saved to {TARGET_SAVE_FILE}")



def load_target():
    check_data_dir()
    if not os.path.exists(TARGET_SAVE_FILE):
        return {}
    try:
        with open(TARGET_SAVE_FILE, "r") as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        return None


def get_target():
    choice = prompt("Do you want to use the saved target? [y/n] ").lower()

    if choice in ("y", "yes", "ye"):
        loading("Loading targets...", 5)
        targets = load_target()
        if not targets:
            print_warning("No saved targets found, please create a new one.")
            return get_target()
        print_info("Saved targets:")
        for i, name in enumerate(targets.keys(), start=1):
            print_info(f"{i}. {name}")

        selection = prompt("Choose a target number: ").strip()
        try:
            selection = int(selection) - 1
            if selection < 0 or selection > len(targets):
                raise ValueError
        except ValueError:
            print_error("Invalid selection")
            return get_target()

        name = list(targets.keys())[selection]
        t = targets[name]
        try:
            check_target(name, t["ip"], t["port"], t["user"])
        except ValueError as e:
            print_error(str(e))
            return get_target()
        passwd = get_pass(f"Password for {t['user']}@{t['ip']}: ")
        return name, t["ip"], t["port"], t["user"], passwd

    elif choice in ("n", "no"):
        name = prompt("Target name: ")
        ip = prompt("Target IP: ")
        port = prompt("Port number: ")
        user = prompt("Username: ")
        try:
            check_target(name, ip, port, user)
        except ValueError as e:
            print_error(str(e))
            return get_target()
        passwd = get_pass(f"Password for {user}@{ip}: ")
        choice = prompt("Do you want to save the target? [y/n] ").lower()
        if choice in ("y", "yes", "ye"):
            save_target(name, ip, port, user)
            return name, ip, port, user, passwd
        elif choice in ("n", "no"):
            return name, ip, port, user, passwd
        else:
            print_error("Invalid selection")
            return get_target()
    else:
        print_error("Invalid selection")
        return get_target()





import os
import json
import ipaddress
import getpass
import sys

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
        confirm = input(f"Target {name} already exists. Overwrite? [y/n] ").lower()
        if confirm not in ["y", "yes"]:
            sys.exit("Saving cancelled")

    targets[name] = {
        "ip": ip,
        "port": port,
        "user": user,
    }

    with open(TARGET_SAVE_FILE, "w") as f:
        json.dump(targets, f, indent=4)

    print(f"Target '{name}' successfully saved to {TARGET_SAVE_FILE}")



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
    choice = input("Do you want to use the saved target? [y/n] ").lower()

    if choice in ("y", "yes", "ye"):
        targets = load_target()
        if not targets:
            print("No saved targets found, please create a new one.")
            return get_target()
        print("Saved targets:")
        for i, name in enumerate(targets.keys(), start=1):
            print(f"{i}. {name}")

        selection = input("Choose a target number: ").strip()
        try:
            selection = int(selection) - 1
            if selection < 0 or selection > len(targets):
                raise ValueError
        except ValueError:
            print("Invalid selection")
            return get_target()

        name = list(targets.keys())[selection]
        t = targets[name]
        check_target(name, t["ip"], t["port"], t["user"])
        passwd = getpass.getpass(f"Password for {t['user']}@{t['ip']}: ")
        return name, t["ip"], t["port"], t["user"], passwd

    elif choice in ("n", "no"):
        name = input("Target name: ")
        ip = input("Target IP: ")
        port = input("Port number: ")
        user = input("Username: ")
        check_target(name, ip, port, user)
        passwd = getpass.getpass(f"Password for {user}@{ip}: ")
        choice = input("Do you want to save the target? [y/n] ").lower()
        if choice in ("y", "yes", "ye"):
            save_target(name, ip, port, user)
            return name, ip, port, user, passwd
        elif choice in ("n", "no"):
            return name, ip, port, user, passwd
        else:
            print("Invalid selection")
            return get_target()
    else:
        print("Invalid selection")
        return get_target()





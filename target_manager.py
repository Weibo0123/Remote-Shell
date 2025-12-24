"""
target_manager.py

This module handles SSH target management for the Remote Shell project.
Support information check, Saving and loading targets.
Provide an interactive interface for selecting or creating targets.
"""
import os
import json
import ipaddress
import sys
from hacker_banner import print_info, print_error, print_success, print_warning, prompt, get_pass, loading

# Directory used to store application data (targets, configs, etc.)
DATA_DIR = "data"
# JSON file used to persist saved SSH targets
TARGET_SAVE_FILE = os.path.join(DATA_DIR, "targets.json")


def check_data_dir():
    """
        Ensure that the data directory exists.
        Creates it if it does not already exist.
    """

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def check_target(name, ip, port, user):
    """
    Check if the information valid
    Raise a value error if not.
    """

    # Check the target name length
    if not (0 < len(name) <= 14):
        raise ValueError("Target name must be between 1 and 14 characters long")

    # Check the IP address format
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise ValueError("Invalid IP address")

    # Check if the port is an integer
    try:
        port = int(port)
    except (TypeError, ValueError):
        raise ValueError("Invalid port number")
    # Check if the port in the range
    if not (1 <= port <= 65535):
        raise ValueError("Port must be between 1 and 65535")

    # Check if the username is empty
    if not user:
        raise ValueError("Username cannot be empty")

def save_target(name, ip, port, user):
    """
    Save the target information to the TARGET_SAVE_FILE.
    if the target already exists, ask user to overwrite it.
    """

    check_data_dir()
    targets = load_target() or {}

    # Handle duplicate target names
    if name in targets:
        confirm = prompt(f"Target {name} already exists. Overwrite? [y/n] ").lower()
        if confirm not in ["y", "yes"]:
            sys.exit("Saving cancelled")

    # Store the target information as a dictionary
    targets[name] = {
        "ip": ip,
        "port": port,
        "user": user,
    }

    # Write targets into the JSON file
    with open(TARGET_SAVE_FILE, "w") as f:
        json.dump(targets, f, indent=4)

    print_success(f"Target '{name}' successfully saved to {TARGET_SAVE_FILE}")



def load_target():
    """
    Load the target information from the TARGET_SAVE_FILE.
    """

    check_data_dir()
    if not os.path.exists(TARGET_SAVE_FILE):
        return {}
    try:
        with open(TARGET_SAVE_FILE, "r") as f:
            return json.load(f)
    except json.decoder.JSONDecodeError:
        return None


def get_target():
    """
    Main interactive target selection flow.
    Allow user to select a saved target or create a new one.
    """

    # Ask user whether to user a saved target
    choice = prompt("Do you want to use the saved target? [y/n] ").lower()

    if choice in ("y", "yes", "ye"):
        # Display animated loading effect before connection
        loading("Loading targets...", 5)
        targets = load_target()
        # Check if the list is empty
        if not targets:
            print_warning("No saved targets found, please create a new one.")
            return get_target()
        # Display the saved targets
        print_info("Saved targets:")
        for i, name in enumerate(targets.keys(), start=1):
            print_info(f"{i}. {name}")

        # Ask user to select a target
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
        # Check the target data before using it
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
        # Check the user input
        try:
            check_target(name, ip, port, user)
        except ValueError as e:
            print_error(str(e))
            return get_target()
        # Ask for password securely
        passwd = get_pass(f"Password for {user}@{ip}: ")
        # Ask whether to save the target
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





# Remote-Shell

## Overview
Remote Shell is a Python-based command-line SSH client designed for interactive remote management with a stylish hacker-inspired interface.

## Project Structure
```
.
├── main.py           # Main application entry point
├── target_manager    # Target management (save, load, check SSH targets)
├── ssh_client.py     # SSH connection handling and interactive shell logic
├── hacker_banner     # I utilities (ASCII banner, colored output, loading animations)
├── requirements.txt  # Python dependencies
├── README.md         # User documentation
└── LICENSE           # Project license
```

## How to Run
1. Clone the repository:
```bash
git clone https://github.com/Weibo0123/Remote-Shell
cd Remote-Shell
```
2. Create a Python virtual environment (optional but recommended):
```bash
python3 -m venv venv
source venv/bin/activate      # Linux / macOS
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run
```bash
python main.py
```

## Dependencies
- Python 3.11
- paramiko
- pyfiglet
- colorama

## Features
- Hacker-style Interface: Displays an ASCII banner and loading animation at startup
- Colorful Output: Different message types use distinct colors (INFO / SUCCESS / WARNING / ERROR)
- Secure Password Input: Passwords are hidden and displayed in a special color for added secrecy
- Target Management: Save, load, and select multiple SSH targets
- SSH Connection: Interact with remote hosts directly in the terminal
- Session Statistics: Shows session duration, bytes sent, and bytes received

## Why I build this
This project was inspired by the book Black Hat Python: Python Programming for Hackers and Pentesters.

While reading the book, I was introduced to many hacking and penetration testing techniques implemented in Python. The section about SSH automation using the Paramiko library
interested me the most.

Instead of following the examples from the book, I want to make this program more usable and user-friendly

As a result, I built Remote Shell — a Python-based SSH tool with a fully functional pseudo-terminal (PTY), interactive input/output, and a hacker-style terminal interface.

# **Warning**
This project is intended **for educational and authorized testing purposes only**.

Remote Shell can be used as an SSH automation and remote management tool, but **using it to access systems without explicit permission is illegal and unethical**.

Always ensure you have **proper authorization** before connecting to any remote system.
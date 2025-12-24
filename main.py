from ssh_client import ssh_session
from target_manager import get_target
from hacker_banner import hacker_banner, startup_sequence

def main():
    """
    Entry point of the Remote Shell application.
    """

    # Display the ASCII hacker banner and project title
    hacker_banner()

    # Run startup animations / initialization sequence
    startup_sequence()

    # Ask user for selecting an existing target or create a new one
    # Returns connection details
    name, ip, port, user, passwd = get_target()

    # Start an interactive SSH session with PTY support
    ssh_session(ip, port, user, passwd)

if __name__ == '__main__':
    main()
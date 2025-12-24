from ssh_client import ssh_session
from target_manager import get_target
from hacker_banner import hacker_banner, startup_sequence

def main():
    hacker_banner()
    startup_sequence()
    #name, ip, port, user, passwd = get_target()
    #ssh_session(ip, port, user, passwd)

if __name__ == '__main__':
    main()
from ssh_client import ssh_session
from target_manager import get_target

def main():
    name, ip, port, user, passwd = get_target()
    ssh_session(ip, port, user, passwd)

if __name__ == '__main__':
    main()

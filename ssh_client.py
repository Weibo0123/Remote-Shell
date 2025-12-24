import paramiko
import sys
import tty
import select
import termios
import os
from hacker_banner import print_info, print_error, print_success, loading

def ssh_session(ip, port, user, password):
    channel = None
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    old_tty = termios.tcgetattr(sys.stdin)

    try:
        loading(text="Connecting", duration=5)
        client.connect(ip, port=port, username=user, password=password)
        channel = client.get_transport().open_session()
        channel.get_pty(term="xterm", width=80, height=24)
        channel.invoke_shell()
        print_success(f"Connected to {user}@{ip}. Type 'exit' to disconnect.")

        tty.setraw(sys.stdin.fileno())

        while True:
            rlist, _, _ = select.select([channel, sys.stdin], [], [])
            if channel in rlist:
                data = channel.recv(1024)
                if not data:
                    break
                sys.stdout.write(data.decode(errors="ignore"))
                sys.stdout.flush()
            if sys.stdin in rlist:
                cmd = os.read(sys.stdin.fileno(), 1024)
                if not cmd:
                    break
                channel.send(cmd)
    except KeyboardInterrupt:
        channel.send("\x03")
    except Exception as e:
        print_error(f"Connection failed: {e}")
        sys.exit()
    finally:
        loading(text="Disconnecting", duration=5)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)
        if channel:
            channel.close()
        client.close()
        print_info("Disconnected")
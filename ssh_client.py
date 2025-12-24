import paramiko
import sys
import tty
import select
import termios
import os

def ssh_session(ip, port, user, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    old_tty = termios.tcgetattr(sys.stdin)

    try:
        client.connect(ip, port=port, username=user, password=password)
        channel = client.get_transport().open_session()
        channel.get_pty(term="xterm", width=80, height=24)
        channel.invoke_shell()

        print(f"Connected to {user}@{ip}. Type 'exit' to disconnect.")

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
        sys.exit(f"Connection failed: {e}")
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)
        channel.close()
        client.close()
        print("Disconnected")
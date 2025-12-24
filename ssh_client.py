"""
ssh_client.py

Provide an interactive SSH session with a real pseudo-terminal(pty).
Supports real-time input and output, Ctrl+C forwarding and terminal restoration.
"""
import paramiko
import sys
import tty
import select
import termios
import os
import time
from hacker_banner import print_info, print_error, print_success, loading

def ssh_session(ip, port, user, password):
    """
    Establish an interactive SSH session with a remote host.
    Use the interactive PTY shell
    Support Real-time input/output forwarding
    """

    # SSH channel
    channel = None

    # Create SSH client
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Session data initialized
    start_time = None
    bytes_received = 0
    bytes_sent = 0

    # Save the current terminal setting
    old_tty = termios.tcgetattr(sys.stdin)

    try:
        # Display connect animation
        loading(text="Connecting", duration=5)
        # Establish SSH connection
        client.connect(ip, port=port, username=user, password=password)
        # Open a new SSH session channel
        channel = client.get_transport().open_session()
        # Request a pseudo-terminal for full shell support
        channel.get_pty(term="xterm", width=80, height=24)
        channel.invoke_shell()
        print_success(f"Connected to {user}@{ip}. Type 'exit' to disconnect.")
        # Record the session start time
        start_time = time.time()

        # Switch local terminal to raw mode
        tty.setraw(sys.stdin.fileno())

        # Main interactive loop
        while True:
            # Wait for input from either SSH channel ot local keyboard
            rlist, _, _ = select.select([channel, sys.stdin], [], [])

            # Handle output data from remote target
            if channel in rlist:
                data = channel.recv(1024)
                bytes_received += len(data)
                if not data:
                    break
                sys.stdout.write(data.decode(errors="ignore"))
                sys.stdout.flush()

            # Handle input data from local keyboard
            if sys.stdin in rlist:
                cmd = os.read(sys.stdin.fileno(), 1024)
                bytes_sent += len(cmd)
                if not cmd:
                    break
                channel.send(cmd)
    # Handle Ctrl+C
    except KeyboardInterrupt:
        channel.send("\x03")
    # Handle authentication errors
    except paramiko.AuthenticationException:
        print_error("Authentication failed (wrong password)")
    # Handle SSH errors
    except paramiko.SSHException as e:
        print_error(f"SSH error: {e}")
    # Handle rest of exceptions
    except Exception as e:
        print_error(f"Unexpected error: {e}")
    finally:
        # Show disconnect animation
        loading(text="Disconnecting", duration=5)
        # Restore the original terminal settings
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)
        # Close SSH chanel if it opens
        if channel:
            channel.close()
        # Close SSH client
        client.close()
        end_time = time.time()
        # Calculate and display the session statistics
        if start_time:
            duration = int(end_time - start_time)
            minutes, seconds = divmod(duration, 60)
            print_info(f"Session started at: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
            print_info(f"Session ended at: {time.strftime('%H:%M:%S', time.localtime(end_time))}")
            print_info(f"Session duration: {minutes:02d}:{seconds:02d}")
        print_info(f"Bytes received: {bytes_received}")
        print_info(f"Bytes sent: {bytes_sent}")
        print_success("Session completed!")

        print_info("Disconnected")
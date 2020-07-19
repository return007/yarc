"""
Launcher script to start the remote control server.

"""

import argparse
import subprocess
import os
import time

from util import get_my_local_addr, log, render_qrcode, get_free_port, UXException


def handle_same_network(my_local_addr=None):
    """
    In this case, we assume that the devices (the machine running this piece
    of code and the mobile device a.k.a. the remote) are on same network.

    This is possible when both the devices share same LAN. This usually boils
    down to the following possible aspects:

     - Both PC and mobile on same Wi-Fi (probably a home router, etc.)
     - PC is connected to internet via Ethernet and has an active hotspot &
       mobile is connected to that hotspot.
     - PC is connected on mobile's hotspot.

    :param my_local_addr:
      Local IPv4 address of the machine running this code/server. In case it is
      ``None``, then it is determined during runtime.
    """
    if not my_local_addr:
        my_local_addr = get_my_local_addr()

    log("\nStarting remote server...\n", color="cyan")
    port = get_free_port()
    addr = f"http://{my_local_addr}:{port}"

    process_command = f"/usr/bin/env python3 app.py --port {port}"

    try:
        proc = subprocess.Popen(
            process_command.split(),
            cwd=os.path.dirname(os.path.realpath(__file__))
        )
    except:
        log("Stopping remote server...", color="red")
        raise

    log("Scan the below code to start using remote.", color="cyan", bold=True)
    render_qrcode(addr)
    log("\n\n")
    log("Or alternatively, write the following URL on your mobile browser:",
        color="cyan", bold=True)
    log(f"\t\t{addr}\n", color="blue", bold=True)

    try:
        log("Are you able to connect to it ? [Y/n]")
        response = input()
        if response.lower() == "n" or response.lower() == "no":
            # User cannot connect via local flow
            # Start "via internet" flow
            raise UXException()
        while proc.poll() is None:
            # As long as the remote server is up
            time.sleep(1)
    except Exception as e:
        # Some eror occurred in the remote server process
        if isinstance(e, UXException):
            # If the exception is raised by the user, then reraise it
            raise
        else:
            # Simply pass, and then gracefully exit
            # Don't forget to print what happened
            log(f"Unexpected failure at remote server process\n"
                f"Remote server process exited with code: {proc.poll()}",
                color="red")
    except BaseException:
        # In case of some interupt from the user, gracefully kill the remote
        # process and then exit
        proc.kill()
        log("Exiting...", color="cyan")


def handle_internet():
    pass


def main():
    """
    Entry point (as usual)

    As of now, we do the following:

     - Disable logging from Flask
     - Start Flask app and let user open their remote and establish connection
    """
    parser = argparse.ArgumentParser(description=__doc__)

    # First, be optimistic and assume both devices are on same network
    # Display QR code to connect to localhost and if succeeds, then hurray!
    try:
        handle_same_network()
    except UXException:
        # Mobile and PC are not on same LAN
        # This flow should handle such cases
        handle_internet()



if __name__ == '__main__':
    main()

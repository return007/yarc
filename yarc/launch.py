#!/usr/bin/env python3
"""
Launcher script to start the remote control server.

"""

import argparse
import os
import threading
import time

from app import run as app_run
from util import get_free_port, get_my_local_addr, log, render_qrcode


def handle_connection(my_local_addr=None):
    """
    Handle connection setup between client and server. There are two possible
    flows:

      1. When devices are in the same local network
      2. When devices are not in the same local network but are reachable
         (indirectly) via public internet.

    Case#1 is easy to handle. The server will run on the PC which needs to be
    controlled while the mobile (aka. controller/client) will connect to server
    and communicate.

    Case#2 is little hard to handle. It relies on a public echo server to
    establish communication between client and server.

    Case#1 possible when both the devices share same LAN. This usually boils
    down to the following possible aspects:

     - Both PC and mobile on same Wi-Fi (probably a home router, etc.)
     - PC is connected to internet via Ethernet and has an active hotspot &
       mobile is connected to that hotspot.
     - PC is connected on mobile's hotspot.

    For simplicity and quicker TAT, I am only working on Case#1. Case#2 will
    need little extra engineering.

    :param my_local_addr:
      Local IPv4 address of the machine running this code/server. In case it is
      ``None``, then it is determined during runtime.
    """
    log("\nStarting control server...\n", color="cyan")
    if not my_local_addr:
        my_local_addr = get_my_local_addr()

    port = get_free_port()
    addr = f"http://{my_local_addr}:{port}"

    try:
        app_thread = threading.Thread(target=app_run, args=(port,),
                                      daemon=True)
        app_thread.start()
    except:
        log("Stopping control server...", color="red")
        raise

    log("Scan the below code to start using remote control.", color="cyan",
        bold=True)
    render_qrcode(addr)
    log("\n\n")
    log("Or alternatively, write the following URL on your mobile browser:",
        color="cyan", bold=True)
    log(f"\t\t{addr}\n", color="blue", bold=True)

    try:
        while app_thread.is_alive():
            time.sleep(1)
    except Exception as e:
        # Simply pass, and then gracefully exit
        # Don't forget to print what happened
        log(f"Unexpected failure at control server process\n"
            f"  {str(e)}", color="red")
        log("Exiting...", color="cyan")
    except BaseException:
        # Simply pass and exit
        log("Exiting...", color="cyan")


def main():
    """
    Entry point (as usual)
    """
    parser = argparse.ArgumentParser(description=__doc__)
    # TODO: Add parsing options (like ``--private-network``,
    #  ``--public-network``)
    handle_connection()


if __name__ == '__main__':
    main()

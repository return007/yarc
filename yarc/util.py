"""
Helper utlities used by yarc server
"""

import socket
import sys

from qrcode import QRCode


COLOR_MAP = {
    'black'    : '\033[90m',
    'red'      : '\033[91m',
    'green'    : '\033[92m',
    'yello'    : '\033[93m',
    'blue'     : '\033[94m',
    'magenta'  : '\033[95m',
    'cyan'     : '\033[96m',
    'white'    : '\033[97m',
}


FORMAT_MAP = {
    'bold'     : '\033[1m',
    'dim'      : '\033[2m',
    'italic'   : '\033[3m',
    'underline': '\033[4m',
    'blink'    : '\033[5m',
}


COMMAND_DELIMITER = '^_^'


def render_qrcode(text):
    """
    Displays a QR code with the given ``text`` on the terminal.
    """
    qr = QRCode()
    qr.add_data(text)
    qr.print_tty()


def get_my_local_addr():
    """
    Returns ``str`` indicating the IPv4 address of the current machine from
    which the function is invoked.

    In case of multiple local addresses, it only returns one of them.

    In case there is no local address (i.e. not connected to internet in any
    form),

    For example:

      >> get_my_local_addr()
      '192.168.1.5'
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
    except:
        raise
    else:
        ip_addr = sock.getsockname()[0]
        sock.close()

    return ip_addr


def log(text, where='stdout', color=None, **fmt_options):
    """
    Logs to ``where`` (default ``stdout``) with the given formatting.

    :param text:
      What to log
    :type text:
      ``str``

    :param where:
      Where to log, can either be ``stdout`` or ``stderr``.

    :param color:
      Which color to use while logging. Can be one of:
      'black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan' & 'white'

    :param fmt_options:
      ``dict`` containing other formatting options like:
      ``{'underline': True, 'bold': False}``
    """
    logto = None
    if where == "stdout":
        logto = sys.stdout
    elif where == "stderr":
        logto = sys.stderr
    else:
        raise ValueError(
            f"Invalid argument value for 'where': {where}\n"
            f"Should be one of 'stdout' or 'stderr'"
        )

    log_statement = text
    if color:
        # If there is no matching color name, then simply ignore and don't
        # color the font
        color_code = COLOR_MAP.get(color.lower(), '\033[0m')
        log_statement = f"{color_code}{text}\033[0m"

    if fmt_options:
        fmt = ""
        for fmt_key in FORMAT_MAP:
            if fmt_options.get(fmt_key):
                fmt += FORMAT_MAP[fmt_key]

        log_statement = f"{fmt}{log_statement}\033[0m"

    logto.write(log_statement)
    logto.write("\n")
    logto.flush()


def get_free_port():
    """
    Get a free open port on the machine. This is not a very optimal solution,
    but just works!
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('', 80))
    except:
        raise
    else:
        port = sock.getsockname()[1]
        sock.close()

    return port

"""
Handles the web-socket based communication between the yarc server and the
remote client.

"""

import asyncio
import pyautogui
import websockets

from websockets.exceptions import ConnectionClosedOK

from util import COMMAND_DELIMITER, log


async def cmove_handler(args):
    """
    ``CMOVE`` command callback.

    Cursor movement happens here.

    :param args:
      The arguments passed from JavaScript corresponding to ``CMOVE`` command.
      It is a comma separated ``str``, containing two values representing
      movement to be done in X,Y directions.

    TODO: Add ability to change movement sensitivity from the settings. For now
     1.5 value seems good enough to handle day-to-day simple tasks.
    """
    MOUSE_SENSITIVITY = 1.5
    delta_x, delta_y = args.strip().split(',')
    move_x = int(int(delta_x) * MOUSE_SENSITIVITY)
    move_y = int(int(delta_y) * MOUSE_SENSITIVITY)
    pyautogui.move(move_x, move_y)


async def click_handler(args):
    """
    ``CLICK`` command callback.

    Mouse click actions happens here.

    :param args:
      The arguments passed from JavaScript corresponding to ``CLICK`` command.
      Possible values: "left"/"right"
    """
    args = args.strip()
    pyautogui.click(button=args)


async def scroll_handler(args):
    """
    ``SCROLL`` command callback.

    Scrolling action happens here. As of now, only vertical scrolling is
    supported.

    :param args:
      The arguments passed from JavaScript corresponding to ``SCROLL`` command,
      indicating movement done in Y direction.

    TODO:
     1. Make sensitivity adjustable from the remote UI.
     2. Scroll inversion adjustment should also be available.
    """
    SCROLL_SENSITIVITY = 0.8
    args = int(int(args.strip()) * SCROLL_SENSITIVITY)
    pyautogui.scroll(args)


async def main(websocket, path):
    """
    Main handler for incoming websocket traffic.

    Listens to incoming command and then directs the traffic to corresponding
    handlers.
    """
    try:
        while True:
            inc_cmd = await websocket.recv()
            command, args = inc_cmd.split(COMMAND_DELIMITER)
            if command == 'CMOVE':
                # Instruction to move the cursor
                # args will contain the delta to move (in both directions)
                await cmove_handler(args)
            elif command == 'CLICK':
                # Instruction to click the mouse button
                # args will contain which mouse button to click
                await click_handler(args)
            elif command == 'SCROLL':
                # Instruction to use mouse scroll
                # args will contain how much to scroll (in vertical direction)
                await scroll_handler(args)

    except ConnectionClosedOK:
        log('WS connection closed by remote!')
        log('  But no worries, you can connect again :)', color='green')


def run(port):
    start_server = websockets.serve(main, "0.0.0.0", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

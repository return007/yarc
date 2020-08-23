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
    SENSITIVITY = 1.5
    delta_x, delta_y = args.strip().split(',')
    move_x = int(int(delta_x) * SENSITIVITY)
    move_y = int(int(delta_y) * SENSITIVITY)
    pyautogui.move(move_x, move_y)


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
    except ConnectionClosedOK:
        log('WS connection closed by remote!')
        log('  But no worries, you can connect again :)', color='green')


def run(port):
    start_server = websockets.serve(main, "0.0.0.0", port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
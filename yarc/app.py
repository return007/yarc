"""
Defines Flask app.
"""

import argparse
import json
import os
import logging
import pyautogui

from flask import Flask, render_template, request

from util import log


app = Flask(__name__)


def disable_flask_logging():
    os.environ['WERKZEUG_RUN_MAIN'] = 'true'
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)


@app.route("/")
def serve_html():
    return render_template("remote.html")


@app.route("/keypress", methods=['POST'])
def keypress_callback():
    """
    Called from UI when a key press event occurs
    """
    data = request.get_json()
    buttonid = data['buttonid']
    assert buttonid in pyautogui.KEYBOARD_KEYS, "Unknown buttonid received"
    pyautogui.press(buttonid)
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


def run(port):
    disable_flask_logging()
    log("Remote server running...", color="cyan")
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--port', default='5050',
        help='Specify port no. to which the Flask app will bind to.'
    )
    args = parser.parse_args()

    run(port=args.port)

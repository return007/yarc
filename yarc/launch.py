"""
Launcher script to start the remote control server.

"""
from flask import Flask, render_template
app = Flask(__name__)

def main():
    app.run(host='0.0.0.0')


@app.route("/")
def serve_html():
    return render_template("remote.html")

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

if __name__ == '__main__':
    main()

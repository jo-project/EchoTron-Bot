import os
import signal

from threading import Thread
from waitress import serve

from flask import render_template, url_for
from flask_express import FlaskExpress

app = FlaskExpress(__name__, template_folder='static')

@app.get("/")
def home(req, res):
    css_url = url_for('static', filename='css/style.css')
    return render_template('404.html', css_url=css_url), 404


def run():
    serve(app, host="0.0.0.0", port=5000)
    
def shutdown():
    try:
        os.system("kill -9 $(ps -A | grep python | awk '{print $1}')")
    except Exception as e:
        print(f'Error stopping bot: {e}')


def keep_alive(message: str ='OK'):
    t = Thread(target=run)
    t.start()
    
    if message:
        @app.route("/custom")
        def custom(req, res):
            return res.send(f'<h1>{message}</h1>')

    def signal_handler(sig, frame):
        print(f'Received signal {sig}. Shutting down server...')
        shutdown()

    # Register signal handlers for SIGINT and SIGTSTP
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTSTP, signal_handler)
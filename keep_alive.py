from threading import Thread

from flask import Flask, current_app

app = Flask("keep_alive")


@app.route("/")
def home():
    return current_app.send_static_file("index.html")


def run():
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
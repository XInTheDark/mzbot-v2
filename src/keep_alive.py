from threading import Thread

from flask import Flask

app = Flask('')


@app.route('/')
def main():
    return "MZ Bot v2 is running..."


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()
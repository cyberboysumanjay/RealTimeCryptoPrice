import json
import os
import time
from datetime import datetime
import requests
from flask import Flask, Response, render_template, send_from_directory


app = Flask(__name__)
API_URL = "https://x.wazirx.com/wazirx-falcon/api/v2.0/crypto_rates"
    

@app.route("/")
def home():
    supported_cryptos = requests.get(API_URL).json().keys()
    return render_template("home.html",supported_cryptos=supported_cryptos)

@app.route("/arc-sw.js")
def arc():
    return send_from_directory(os.getcwd()+"/static","arc-sw.js")



@app.route("/<crypto>")
def index(crypto):
    supported_cryptos = requests.get(API_URL).json().keys()
    if crypto.lower() in supported_cryptos:
        return render_template("index.html",crypto=crypto)
    return "This Cryptocurrency is not yet supported!"


def generate_random_data(crypto_code):
    while True:
        price = float(requests.get(API_URL).json()[crypto_code]['inr'])
        json_data = json.dumps(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "value": price,
            }
        )
        yield f"data:{json_data}\n\n"
        time.sleep(15)


@app.route("/chart-data/<crypto>")
def chart_data(crypto):
    return Response(generate_random_data(crypto), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, threaded=True)

import os
import time
import json
import requests
import threading
from datetime import datetime
from prometheus_client import Gauge, make_wsgi_app
from wsgiref.simple_server import make_server

RPC_ENDPOINT = os.getenv("RPC_ENDPOINT", "https://api.mainnet-beta.solana.com")

# Raise an error if the WALLET environment variable is not set
if "WALLET" not in os.environ or os.environ["WALLET"].strip() == "":
    raise ValueError("The WALLET environment variable must be set and not empty.")

WALLET = os.environ["WALLET"]

LAMPORTS_PER_SOL = 1000000000

headers = {
    "Content-Type": "application/json"
}

data = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getBalance",
    "params": [WALLET]
}

# Create a Prometheus Gauge metric named 'wallet_balance'
wallet_balance = Gauge('wallet_balance', 'Wallet balance in SOL')

# Create a WSGI app that serves the Prometheus metrics
app = make_wsgi_app()

# Start an HTTP server on port 8000 with a custom handler for the /metrics endpoint
httpd = make_server('', 8000, app)
httpd_thread = threading.Thread(target=httpd.serve_forever)
httpd_thread.daemon = True
httpd_thread.start()

while True:
    response = requests.post(RPC_ENDPOINT, headers=headers, json=data)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code} from the server.")
    else:
        result = response.json()

    if 'result' in result and 'value' in result['result']:
        balance = int(result['result']['value'])
        sol_balance = balance / LAMPORTS_PER_SOL

        # Update the metric with the current balance value
        wallet_balance.set(sol_balance)

        current_date = datetime.now().strftime("%D %T")
        output = {
            "date": f"{current_date}",
            "balance": sol_balance
        }

        print(json.dumps(output))
    else:
        print(f"Error: Unexpected response format: {result}.. Wallet address might be wrong")
    time.sleep(30)

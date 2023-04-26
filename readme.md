# Solana Wallet Balance Monitor

This Python script monitors the balance of a Solana wallet and exposes the balance as a Prometheus metric.
The wallet address is specified using the `WALLET` environment variable.
The script also supports an optional `RPC_ENDPOINT` environment variable to specify a custom Solana RPC endpoint _defaults to "https://api.mainnet-beta.solana.com"_

## Features

- Retrieves the balance of a Solana wallet using the Solana JSON-RPC API
- Exposes the wallet balance as a Prometheus Gauge metric named `wallet_balance`
- Starts an HTTP server on port 8000 with a custom handler for the `/metrics` endpoint to serve the Prometheus metrics
- Prints the current date and wallet balance to the console every 30 seconds

## Requirements

- Python 3.x
- The following Python packages:
  - `requests`
  - `prometheus_client`

## Usage

1. Install the required Python packages:

```bash
pip3 install -r requirements.txt
```

2. Set the `WALLET` environment variable to the desired Solana wallet address:

```bash
export WALLET="your_wallet_address"
```

3. (Optional) Set the `RPC_ENDPOINT` environment variable to a custom Solana RPC endpoint:

```bash
export RPC_ENDPOINT="your_custom_rpc_endpoint"
```

4. Run the script:
```bash
python3 watch.py
```

Check the metrics
```bash
curl -i -s http://localhost:8000/metrics
```


## Running from docker
```bash
docker run -p 8000:8000 -e WALLET=<your-wallet> holaplex/sol-balance-exporter:latest
```

Query metrics
```bash
~> curl -i -s localhost:8000/metrics | grep -i balance
# HELP wallet_balance Wallet balance in SOL
# TYPE wallet_balance gauge
wallet_balance 0.27712856
```

# Binance Futures Testnet Trading Bot

A clean, structured Python CLI application that places **Market**, **Limit**, and **Stop-Limit** orders on the Binance Futures Testnet (USDT-M).

---

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py
│   ├── client.py          # Binance API wrapper
│   ├── orders.py          # Order placement logic
│   ├── validators.py      # Input validation
│   └── logging_config.py  # Logging setup
├── logs/                  # Auto-created on first run
├── cli.py                 # CLI entry point
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Clone the project

```bash
cd trading_bot
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Bot

### Market Order
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Limit Order
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 80000
```

### Stop-Limit Order *(bonus)*
```bash
python cli.py --symbol BTCUSDT --side BUY --type STOP --quantity 0.01 --price 95000 --stop-price 94000
```
---

## Logs

All API requests, responses, and errors are logged to `logs/trading_YYYYMMDD.log`.

---

## Assumptions

- Testnet base URL: `https://testnet.binancefuture.com/fapi`
- All orders use `timeInForce=GTC` for LIMIT and STOP types
- Credentials are loaded from a `.env` file in the project root
- Python 3.10+
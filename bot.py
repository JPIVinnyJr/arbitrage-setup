import os
import ccxt
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET = os.getenv("BINANCE_SECRET")
BYBIT_API_KEY = os.getenv("BYBIT_API_KEY")
BYBIT_SECRET = os.getenv("BYBIT_SECRET")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Exchange setup
binance = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET,
})

bybit = ccxt.bybit({
    'apiKey': BYBIT_API_KEY,
    'secret': BYBIT_SECRET,
})

symbols = ["BTC/USDT", "ETH/USDT", "BCH/USDT"]
profit_threshold = 0.5  # in percent

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except:
        pass

def check_arbitrage():
    for symbol in symbols:
        try:
            price_binance = binance.fetch_ticker(symbol)['ask']
            price_bybit = bybit.fetch_ticker(symbol)['bid']

            if price_binance == 0 or price_bybit == 0:
                continue

            diff = price_bybit - price_binance
            percent = (diff / price_binance) * 100

            if percent >= profit_threshold:
                msg = f"Arbitrage Opportunity: {symbol}\nBuy on Binance: {price_binance}\nSell on Bybit: {price_bybit}\nProfit: {percent:.2f}%"
                print(msg)
                send_telegram(msg)

        except Exception as e:
            print(f"Error checking {symbol}: {e}")

while True:
    check_arbitrage()
    time.sleep(15)

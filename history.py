import os
import time

import pandas as pd
import yfinance as yf


def _get_prices_remote(ticker, filename):
    print(f"Fetching {ticker} from yfinance...")

    yf_ticker = yf.Ticker(ticker)
    prices = yf_ticker.history(period="max")

    prices.reset_index().to_csv(filename, index=False)

    return prices


def get_prices(ticker, datadir="data"):
    file_name = f"{datadir}/{ticker}.csv"

    if not os.path.exists(file_name):
        return _get_prices_remote(ticker, file_name)

    now = time.time()
    stat = os.stat(file_name)
    if (now - stat.st_mtime) > (60 * 60 * 24):
        return _get_prices_remote(ticker, file_name)

    prices = pd.read_csv(file_name)
    prices["Date"] = pd.to_datetime(prices["Date"])
    prices = prices.set_index("Date")

    return prices

import pandas as pd
import yfinance as yf


def fetch_ohlcv_data(tickers: list[str], start_date: str, end_date: str, output_file: str = "ohlcv_data.csv") -> pd.DataFrame:
    """Fetch adjusted close prices and save to CSV."""
    try:
        data = yf.download(tickers, start=start_date, end=end_date, progress=False)["Adj Close"]
        data.dropna(how="all", inplace=True)
        data.to_csv(output_file)
    except Exception as e:
        print(f"Error fetching data for tickers {tickers}: {e}")
    return data


def main():
    tickers = ["KO", "PEP", "AAPL", "MSFT"]
    fetch_ohlcv_data(tickers, "2018-01-01", "2023-12-31")


if __name__ == "__main__":
    main()

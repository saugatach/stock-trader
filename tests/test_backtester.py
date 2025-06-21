import pandas as pd
from datetime import datetime
from pairs_trading import backtester


def test_backtest_signals(tmp_path):
    dates = pd.date_range("2020-01-01", periods=3)
    prices = pd.DataFrame({"A": [10, 11, 12], "B": [8, 9, 10]}, index=dates)
    prices_file = tmp_path / "prices.csv"
    prices.to_csv(prices_file)

    signals = pd.DataFrame({
        "Date": [dates[0], dates[2]],
        "Ticker_A": ["A", "A"],
        "Ticker_B": ["B", "B"],
        "ZScore": [-1.2, 0.2],
        "Signal": ["LongSpread", "Exit"],
    })
    signals_file = tmp_path / "signals.csv"
    signals.to_csv(signals_file, index=False)

    trades = backtester.backtest_signals(data_file=str(prices_file), signals_file=str(signals_file), output_file=str(tmp_path/"trades.csv"))
    assert len(trades) == 1
    assert {"EntryDate", "ExitDate", "Ticker_A", "Ticker_B", "Direction", "PnL"}.issubset(trades.columns)

import pandas as pd
from pairs_trading import signal_generator


def test_generate_signals(tmp_path, monkeypatch):
    dates = pd.date_range("2020-01-01", periods=9)
    diffs = [0]*3 + [-3]*3 + [0]*3
    a = pd.Series(range(9), index=dates)
    b = a - diffs
    prices = pd.DataFrame({"A": a, "B": b})
    data_file = tmp_path / "prices.csv"
    prices.to_csv(data_file)
    pairs_file = tmp_path / "pairs.csv"
    pd.DataFrame({"Ticker_A": ["A"], "Ticker_B": ["B"], "PValue": [0.01]}).to_csv(pairs_file, index=False)

    monkeypatch.setattr(signal_generator, "ROLLING_WINDOW", 3)
    out_file = tmp_path / "signals.csv"
    df = signal_generator.generate_signals(data_file=str(data_file), pairs_file=str(pairs_file), output_file=str(out_file))

    assert not df.empty
    assert {"Date", "Ticker_A", "Ticker_B", "ZScore", "Signal"}.issubset(df.columns)
    assert set(df["Signal"]).issubset({"LongSpread", "ShortSpread", "Exit"})

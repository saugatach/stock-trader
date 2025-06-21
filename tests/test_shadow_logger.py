import pandas as pd
from datetime import datetime
from pairs_trading import shadow_logger


def test_log_today_signals(tmp_path, monkeypatch):
    today = datetime.utcnow().date()
    signals = pd.DataFrame({
        "Date": [pd.Timestamp(today)],
        "Ticker_A": ["A"],
        "Ticker_B": ["B"],
        "ZScore": [0.5],
        "Signal": ["Exit"],
    })
    signals_file = tmp_path / "signals.csv"
    signals.to_csv(signals_file, index=False)

    out_file = tmp_path / "shadow.csv"
    logged = shadow_logger.log_today_signals(signals_file=str(signals_file), output_file=str(out_file))
    assert len(logged) == 1
    loaded = pd.read_csv(out_file)
    assert len(loaded) == 1

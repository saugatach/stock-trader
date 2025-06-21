from datetime import datetime
import pandas as pd


def log_today_signals(
    signals_file: str = "signal_log.csv",
    output_file: str = "shadow_trades.csv",
) -> pd.DataFrame:
    today = datetime.utcnow().date()
    signals = pd.read_csv(signals_file, parse_dates=["Date"])
    today_signals = signals[signals["Date"].dt.date == today]
    if today_signals.empty:
        return pd.DataFrame()

    try:
        existing = pd.read_csv(output_file)
        combined = pd.concat([existing, today_signals], ignore_index=True)
    except FileNotFoundError:
        combined = today_signals

    combined.to_csv(output_file, index=False)
    return today_signals


def main():
    log_today_signals()


if __name__ == "__main__":
    main()

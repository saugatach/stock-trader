import argparse
from pairs_trading.data_loader import fetch_ohlcv_data
from pairs_trading.pair_selector import select_cointegrated_pairs
from pairs_trading.signal_generator import generate_signals
from pairs_trading.backtester import backtest_signals
from pairs_trading.shadow_logger import log_today_signals


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Pairs Trading Pipeline")
    parser.add_argument("--fetch-data", action="store_true")
    parser.add_argument("--select-pairs", action="store_true")
    parser.add_argument("--generate-signals", action="store_true")
    parser.add_argument("--backtest", action="store_true")
    parser.add_argument("--shadow-log", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    print("Starting pipeline...")
    if args.fetch_data:
        fetch_ohlcv_data(["KO", "PEP", "AAPL", "MSFT"], "2020-06-30", "2025-06-10")
    if args.select_pairs:
        select_cointegrated_pairs()
    if args.generate_signals:
        generate_signals()
    if args.backtest:
        backtest_signals()
    if args.shadow_log:
        log_today_signals()


if __name__ == "__main__":
    main()

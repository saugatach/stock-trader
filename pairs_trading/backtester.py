import pandas as pd

ALLOCATION = 10000
SLIPPAGE = 0.001


def backtest_signals(
    data_file: str = "./pairs_trading/ohlcv_data.csv",
    signals_file: str = "./pairs_trading/signal_log.csv",
    output_file: str = "./pairs_trading/backtest_trades.csv",
) -> pd.DataFrame:
    prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
    signals = pd.read_csv(signals_file, parse_dates=["Date"])

    trades = []
    positions = {}
    for _, row in signals.iterrows():
        key = (row["Ticker_A"], row["Ticker_B"])
        date = row["Date"]
        price_a = prices.loc[date, row["Ticker_A"]]
        price_b = prices.loc[date, row["Ticker_B"]]

        if row["Signal"] in ["LongSpread", "ShortSpread"]:
            positions[key] = {
                "EntryDate": date,
                "Direction": row["Signal"],
                "PriceA": price_a,
                "PriceB": price_b,
            }
        elif row["Signal"] == "Exit" and key in positions:
            pos = positions.pop(key)
            entry_spread = pos["PriceA"] - price_b if pos["Direction"] == "LongSpread" else price_a - pos["PriceB"]
            exit_spread = price_a - price_b
            if pos["Direction"] == "LongSpread":
                pnl = (exit_spread - entry_spread)
            else:
                pnl = (entry_spread - exit_spread)
            pnl *= ALLOCATION
            pnl -= abs(pnl) * SLIPPAGE
            trades.append({
                "EntryDate": pos["EntryDate"].strftime("%Y-%m-%d"),
                "ExitDate": date.strftime("%Y-%m-%d"),
                "Ticker_A": key[0],
                "Ticker_B": key[1],
                "Direction": pos["Direction"],
                "PnL": round(pnl, 2),
            })

    trades_df = pd.DataFrame(trades)
    trades_df.to_csv(output_file, index=False)
    return trades_df


def main():
    backtest_signals()


if __name__ == "__main__":
    main()

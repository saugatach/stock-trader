import pandas as pd
import numpy as np
import statsmodels.api as sm


ENTRY_Z = 1
EXIT_Z = 0
ROLLING_WINDOW = 30


def hedge_ratio(series_a: pd.Series, series_b: pd.Series) -> float:
    model = sm.OLS(series_a, sm.add_constant(series_b)).fit()
    return model.params[1]


def generate_signals(
    data_file: str = "ohlcv_data.csv",
    pairs_file: str = "selected_pairs.csv",
    output_file: str = "signal_log.csv",
) -> pd.DataFrame:
    prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
    pairs = pd.read_csv(pairs_file)

    logs = []
    for _, row in pairs.iterrows():
        a, b = row["Ticker_A"], row["Ticker_B"]
        series_a = prices[a]
        series_b = prices[b]
        beta = hedge_ratio(series_a, series_b)
        spread = series_a - beta * series_b
        zscore = (spread - spread.rolling(ROLLING_WINDOW).mean()) / spread.rolling(ROLLING_WINDOW).std()

        position = None
        for date, z in zscore.dropna().items():
            signal = ""
            if position is None:
                if z < -ENTRY_Z:
                    position = "LongSpread"
                    signal = position
                elif z > ENTRY_Z:
                    position = "ShortSpread"
                    signal = position
            else:
                if (position == "LongSpread" and z > EXIT_Z) or (
                    position == "ShortSpread" and z < -EXIT_Z
                ):
                    signal = "Exit"
                    position = None
            if signal:
                logs.append({
                    "Date": date.strftime("%Y-%m-%d"),
                    "Ticker_A": a,
                    "Ticker_B": b,
                    "ZScore": round(z, 4),
                    "Signal": signal,
                })

    log_df = pd.DataFrame(logs)
    log_df.to_csv(output_file, index=False)
    return log_df


def main():
    generate_signals()


if __name__ == "__main__":
    main()

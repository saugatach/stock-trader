import itertools
import pandas as pd
from statsmodels.tsa.stattools import coint


def select_cointegrated_pairs(
    data_file: str = "ohlcv_data.csv",
    pvalue_threshold: float = 0.05,
    output_file: str = "selected_pairs.csv",
) -> pd.DataFrame:
    """Test all pairs for cointegration and save to CSV."""
    prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
    tickers = prices.columns.tolist()

    rows = []
    for a, b in itertools.combinations(tickers, 2):
        series_a = prices[a]
        series_b = prices[b]
        result = coint(series_a, series_b)
        pvalue = result[1]
        if pvalue < pvalue_threshold:
            rows.append({"Ticker_A": a, "Ticker_B": b, "PValue": pvalue})

    result_df = pd.DataFrame(rows)
    result_df.to_csv(output_file, index=False)
    return result_df


def main():
    select_cointegrated_pairs()


if __name__ == "__main__":
    main()

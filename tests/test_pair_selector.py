import numpy as np
import pandas as pd
from pairs_trading import pair_selector


def test_select_cointegrated_pairs(tmp_path):
    np.random.seed(0)
    n = 100
    x = np.cumsum(np.random.normal(size=n))
    y = x + np.random.normal(scale=0.1, size=n)
    z = np.random.normal(size=n)
    df = pd.DataFrame({"A": x, "B": y, "C": z})
    data_file = tmp_path / "prices.csv"
    df.to_csv(data_file)

    result = pair_selector.select_cointegrated_pairs(data_file=str(data_file), pvalue_threshold=0.05, output_file=str(tmp_path / "pairs.csv"))
    assert not result.empty
    assert {"Ticker_A", "Ticker_B", "PValue"}.issubset(result.columns)
    assert ((result["Ticker_A"] == "A") & (result["Ticker_B"] == "B")).any() or ((result["Ticker_A"] == "B") & (result["Ticker_B"] == "A")).any()

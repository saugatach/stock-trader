import itertools
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint
import set_root
import utils.load_config
from scipy.stats import zscore
from utils.file_utils import clean_path
from numpy.linalg import LinAlgError

def select_cointegrated_pairs(
    data_file: str = "ohlcv_data.csv",
    pvalue_threshold: float = 0.05,
    output_file: str = "selected_pairs.csv",
) -> pd.DataFrame:
    """Test all pairs for cointegration and save to CSV."""
    project_root = set_root.project_root
    config = utils.load_config.load_config(project_root=project_root, verbose=True)
    
    data_file = config.get('ohlcv_data_file', 'ohlcv_data.csv')
    output_file = config.get('selected_pairs_file', 'selected_pairs.csv')
    
    data_file = clean_path(data_file, config)
    output_file = clean_path(output_file, config)
    
    prices = pd.read_csv(data_file, index_col=0, parse_dates=True)
    # print(prices)
    
    # Filter columns that start with 'Close'
    filtered_prices = prices.filter(like='Close')
    tickers = filtered_prices.columns.str.replace('Close_', '', regex=False).tolist()
    print(tickers)
    
    # Rename the columns to remove 'Close_'
    prices = filtered_prices.rename(columns=lambda x: x.replace('Close_', ''))
    
    if prices.isnull().values.any():
        print("Rows with NaN values:")
        print(prices[prices.isnull().any(axis=1)])
    
    # Handle NaN values before normalization
    # First forward fill, then backward fill any remaining NaNs
    # Forward fill NaN values
    prices_filled = prices.copy()
    prices_filled = prices_filled.ffill().bfill()
    
    print(prices_filled)
    
    rows = []
    for a, b in itertools.combinations(tickers, 2):
        series_a = prices_filled[a]
        series_b = prices_filled[b]
        
        try:
            result = coint(series_a, series_b)
            print(result)
            pvalue = result[1]
            if pvalue < pvalue_threshold:
                rows.append({"Ticker_A": a, "Ticker_B": b, "PValue": pvalue})
        except LinAlgError as e:
            print(f"Skipping pair ({a}, {b}) due to linear algebra error: {e}")
            continue
        except Exception as e:
            print(f"Skipping pair ({a}, {b}) due to error: {e}")
    
    result_df = pd.DataFrame(rows)
    print(result_df)
    result_df.to_csv(output_file, index=False)
    print(f"Writing to file {output_file}")
    return result_df

def main():
    select_cointegrated_pairs()

if __name__ == "__main__":
    main()

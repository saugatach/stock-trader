# must run set_root to set the root
import set_root
import sys
print(sys.path)
import utils.load_config

import pandas as pd
from stockanalysis import getstockdata as gd
from stockanalysis import helpers

def fetch_ohlcv_data(tickers: list[str], start_date: str, end_date: str, output_file: str = None, verbose=True) -> pd.DataFrame:
    """Fetch adjusted close prices and save to CSV."""
    settings = helpers.load_settings_stocks()
    project_root = set_root.project_root
    config = utils.load_config.load_config(project_root=project_root, verbose=verbose)

    stockobj = gd.GetStockData(tickers, settings=settings, verbose=verbose)
    data = stockobj.getdata(start=start_date, end=end_date)
    # print(data)
    temp_data = data.copy()
    temp_data.dropna(how="all", inplace=True)
    data = temp_data
    output_file = config['data'] + '/' + config.get('ohlcv_data_file', 'ohlcv_data.csv')
    data.to_csv(output_file, index=True)
    return data


def main():
    tickers = ["KO", "PEP", "AAPL", "MSFT"]
    fetch_ohlcv_data(tickers, "2018-01-01", "2023-12-31")


if __name__ == "__main__":
    main()

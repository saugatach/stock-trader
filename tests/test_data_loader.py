import pandas as pd
import pandas.testing as pdt
from pairs_trading import data_loader


def test_fetch_ohlcv_data(tmp_path, monkeypatch):
    tickers = ["AAA", "BBB"]
    index = pd.date_range("2020-01-01", periods=3)
    cols = pd.MultiIndex.from_product([["Adj Close"], tickers])
    fake = pd.DataFrame([[1, 4], [2, 5], [3, 6]], index=index, columns=cols)

    def fake_download(tickers, start, end, progress=False):
        return fake

    monkeypatch.setattr(data_loader.yf, "download", fake_download)
    out_file = tmp_path / "out.csv"
    df = data_loader.fetch_ohlcv_data(tickers, "2020-01-01", "2020-01-04", output_file=str(out_file))

    expected = fake["Adj Close"]
    pdt.assert_frame_equal(df, expected, check_freq=False)
    loaded = pd.read_csv(out_file, index_col=0, parse_dates=True)
    pdt.assert_frame_equal(loaded, expected, check_freq=False)

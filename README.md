# stock-trader

## Overview
This project implements a cointegration based statistical arbitrage system. It follows the PRD outlined in [docs/codex_instructions.md](docs/codex_instructions.md) and provides a fully offline pipeline for pairs trading analysis. The pipeline downloads price data, selects cointegrated pairs, generates trading signals, runs a backtest, and logs daily signals for shadow trading. An optional Streamlit dashboard visualizes trades and signals.

## Modules
- **data_loader.py** – fetches adjusted close prices with `yfinance` and saves to `ohlcv_data.csv`.
- **pair_selector.py** – tests all ticker pairs for cointegration and writes significant pairs to `selected_pairs.csv`.
- **signal_generator.py** – calculates z‑score based signals using a 30‑day window and records them in `signal_log.csv`.
- **backtester.py** – simulates trade PnL from signals and stores the results in `backtest_trades.csv`.
- **shadow_logger.py** – appends today’s signals to `shadow_trades.csv` for monitoring.
- **streamlit_dashboard.py** – displays the equity curve and recent signals interactively.
- **main.py** – CLI wrapper to run each step of the pipeline.

## Usage
Install requirements (preferably inside a virtual environment):

```bash
pip install -r pairs_trading/requirements.txt
```

Run the entire pipeline:

```bash
python -m pairs_trading.main --fetch-data --select-pairs --generate-signals --backtest --shadow-log
```

Launch the dashboard to inspect results:

```bash
streamlit run pairs_trading/streamlit_dashboard.py
```

## Running Tests
Compile the code and execute the unit tests from the repository root:

```bash
python -m py_compile pairs_trading/*.py
pytest -q
```
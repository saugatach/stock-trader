# 🤖 AGENTIC CODE GENERATION MASTER PLAN

---

### 🧠 GLOBAL MISSION CONTEXT (PROBLEM STATEMENT)

You are tasked with building a complete, modular, and backtestable **cointegration-based statistical arbitrage system**.
This system simulates a hedge fund-style pairs trading strategy, identifying cointegrated stock pairs and executing mean-reverting trades.

The pipeline must be:

* **Fully offline and testable** using CSV files and public price data
* Designed to run either step-by-step via CLI or end-to-end through automation
* Equipped with an **interactive Streamlit dashboard** to allow human evaluation of signals, equity curve, and trades
* **Modular enough for extension** later into live trading or options overlays

**⚠️ Override any generic design biases**:

* Prioritize speed, transparency, and CSV-based traceability
* Avoid overengineering (no databases or web frameworks outside Streamlit)
* Assume no human intervention unless manually running CLI or Streamlit

---

## ✅ PROJECT OUTPUT

You must deliver the following:

### 📁 Project Folder: `pairs_trading/`

```
pairs_trading/
├── main.py
├── data_loader.py
├── pair_selector.py
├── signal_generator.py
├── backtester.py
├── shadow_logger.py
├── streamlit_dashboard.py
├── ohlcv_data.csv
├── selected_pairs.csv
├── signal_log.csv
├── backtest_trades.csv
├── shadow_trades.csv
└── requirements.txt
```

---

## ✅ SYSTEM MODULES & RESPONSIBILITIES

| Module                   | Responsibility                                                       |
| ------------------------ | -------------------------------------------------------------------- |
| `data_loader.py`         | Download and save historical adjusted close prices                   |
| `pair_selector.py`       | Test all ticker pairs for cointegration and save those with p < 0.05 |
| `signal_generator.py`    | Calculate z-score of spread and generate long/short/exit signals     |
| `backtester.py`          | Simulate trade PnL based on signals and compute performance metrics  |
| `shadow_logger.py`       | Append today's signals to a shadow trading log                       |
| `streamlit_dashboard.py` | Display equity curve, signal charts, and performance interactively   |
| `main.py`                | Orchestrate pipeline via CLI flags                                   |

---

## ✅ DATA SPECIFICATION

### `ohlcv_data.csv`

* Columns: one per ticker (e.g., `AAPL`, `MSFT`, etc.)
* Index: Date
* Values: Adjusted Close prices

### `selected_pairs.csv`

```
Ticker_A,Ticker_B,PValue
KO,PEP,0.0321
AAPL,MSFT,0.0212
...
```

### `signal_log.csv`

```
Date,Ticker_A,Ticker_B,ZScore,Signal
2023-06-20,KO,PEP,-1.42,LongSpread
2023-06-27,KO,PEP,0.01,Exit
...
```

### `backtest_trades.csv`

```
EntryDate,ExitDate,Ticker_A,Ticker_B,Direction,PnL
2023-06-20,2023-06-27,KO,PEP,LongSpread,45.23
...
```

### `shadow_trades.csv`

(Same format as `signal_log.csv`, filtered to today’s date)

---

## ✅ SEQUENCE OF EXECUTION (STEP-BY-STEP)

1. `python main.py --fetch-data`
   ⟶ Calls `data_loader.py` to fetch adjusted close prices for selected tickers using yfinance.

2. `python main.py --select-pairs`
   ⟶ Calls `pair_selector.py` to test Engle-Granger cointegration on all pairs and store results.

3. `python main.py --generate-signals`
   ⟶ Calls `signal_generator.py` to generate z-score-based trade signals.

4. `python main.py --backtest`
   ⟶ Calls `backtester.py` to simulate entry/exit trades and save PnL results.

5. `python main.py --shadow-log`
   ⟶ Calls `shadow_logger.py` to record today’s active signals for review.

6. `streamlit run streamlit_dashboard.py`
   ⟶ Launches the interactive visualization layer.

---

## ✅ CONSTRAINTS & ASSUMPTIONS

* All signals and trades are executed **at daily close** only
* Spread is defined as `spread = A - βB`, where `β` is the OLS hedge ratio
* Rolling window for z-score is **30 days**
* Entry Thresholds: `z < -1` (LongSpread), `z > +1` (ShortSpread)
* Exit Threshold: `z` crosses 0
* Backtest slippage = 0.1%; allocation = \$10,000 per trade

---

## ✅ STRATEGIC CODING GUIDELINES

* **Every Python file must define at least one top-level function** for testability
* **Use only CSV and Streamlit for I/O and UI**
* **Avoid global variables**
* **Use hardcoded tickers (e.g., \['KO', 'PEP', 'AAPL', 'MSFT']) for first version**
* Parse dates properly when reading/writing CSVs

---

## ✅ NEXT STEP

Begin with `data_loader.py`, and implement:

```python
def fetch_ohlcv_data(tickers: list[str], start_date: str, end_date: str, output_file: str = "ohlcv_data.csv") -> pd.DataFrame:
    ...
```

Once complete, move to `pair_selector.py`, then `signal_generator.py`, and so on.

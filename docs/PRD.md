Certainly. Here's the **final, polished PRD** for the Cointegration-Based Pairs Trading System with a Streamlit dashboard:

---

# 🧾 PRD: Cointegration-Based Pairs Trading System (with Streamlit Dashboard)

---

## 1. 💡 Project Overview

Build a cointegration-based statistical arbitrage trading pipeline that:

* Fetches daily equity price data
* Identifies cointegrated pairs
* Generates mean-reversion trading signals
* Backtests the strategy with performance metrics
* Displays all analytics via an interactive **Streamlit dashboard**
* (Optional) Supports shadow trading and live broker API integration later

---

## 2. 🎯 Goals

* ✅ Identify cointegrated stock pairs from a user-defined universe
* ✅ Generate signals using z-score of hedge-ratio adjusted spread
* ✅ Backtest trades with performance tracking
* ✅ Log daily signals for shadow (paper) trading
* ✅ Provide an interactive, modular dashboard for visualization

---

## 3. ⚙️ Tech Stack

| Component     | Technology                           |
| ------------- | ------------------------------------ |
| Data Source   | `yfinance`                           |
| Stats Library | `statsmodels`, `scikit-learn`        |
| Signal Logic  | `pandas`, `numpy`                    |
| Backtesting   | Custom logic (no external framework) |
| Dashboard     | `Streamlit`                          |
| Visualization | `matplotlib`, `plotly` (optional)    |
| CLI           | `argparse`                           |
| Language      | Python 3.10+                         |

---

## 4. 📁 Folder and File Structure

```bash
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

## 5. 🧠 Strategy Logic

### 5.1 Cointegration

* Test all stock pairs using Engle-Granger (`statsmodels.tsa.stattools.coint`)
* Accept pairs with **p-value < 0.05**
* Output top N pairs to `selected_pairs.csv`

### 5.2 Spread & Hedge Ratio

* Regress A \~ B using OLS → get hedge ratio `β`
* Compute spread: `spread_t = A_t - β * B_t`

### 5.3 Z-score Signal Generation

* Rolling window (30 days):

  ```python
  z_score = (spread_t - mean(spread_window)) / std(spread_window)
  ```
* Signal Rules:

  * z < -1 → Long Spread
  * z > +1 → Short Spread
  * z crosses 0 → Exit

---

## 6. 📦 Output Files

| File Name             | Description                            |
| --------------------- | -------------------------------------- |
| `ohlcv_data.csv`      | Clean daily price data for all tickers |
| `selected_pairs.csv`  | Cointegrated pair list and p-values    |
| `signal_log.csv`      | Signal history with z-scores           |
| `backtest_trades.csv` | Trade PnL, entry/exit, Sharpe          |
| `shadow_trades.csv`   | Paper trade signals for live tracking  |

---

## 7. 📊 Streamlit Dashboard (`streamlit_dashboard.py`)

### Sidebar:

* Select ticker pair (dropdown)
* Choose time range (slider)
* Toggle: only active trades or all dates

### Tabs:

1. **Equity Curve** – Cumulative return chart
2. **Signal Chart** – Z-score, spread, and signal markers
3. **Performance Stats** – Sharpe, win rate, drawdown
4. **Trade Log** – Table from `backtest_trades.csv`
5. **Signal Log** – Table from `signal_log.csv`

---

## 8. 🛠 Requirements

```txt
pandas
numpy
yfinance
statsmodels
scikit-learn
matplotlib
streamlit
```

---

## 9. 🧪 Assumptions

* All trades entered at daily close
* Capital is equally allocated per trade
* No leverage or shorting constraints
* No transaction costs assumed initially
* Shadow trade logs are not executed—just saved for analysis

---
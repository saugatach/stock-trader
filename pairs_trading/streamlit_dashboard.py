import pandas as pd
import streamlit as st


def load_data():
    trades = pd.read_csv("backtest_trades.csv")
    signals = pd.read_csv("signal_log.csv")
    return trades, signals


def main():
    st.title("Pairs Trading Dashboard")
    trades, signals = load_data()

    if not trades.empty:
        st.subheader("Equity Curve")
        trades["CumulativePnL"] = trades["PnL"].cumsum()
        st.line_chart(trades.set_index("ExitDate")["CumulativePnL"])

    st.subheader("Recent Signals")
    st.dataframe(signals.tail(10))


if __name__ == "__main__":
    main()

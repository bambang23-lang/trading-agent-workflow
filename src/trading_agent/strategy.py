from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .indicators import compute_macd, compute_rsi, compute_sma


@dataclass(frozen=True)
class SignalDecision:
    action: str
    reason: str
    confidence: float
    price: float


def generate_signal(df: pd.DataFrame, short_window: int = 20, long_window: int = 50, rsi_period: int = 14) -> SignalDecision:
    if df.empty:
        return SignalDecision("HOLD", "No data", 0.0, 0.0)

    data = df.copy()
    data["sma_short"] = compute_sma(data["close"], short_window)
    data["sma_long"] = compute_sma(data["close"], long_window)
    data["rsi"] = compute_rsi(data["close"], rsi_period)
    macd_line, signal_line = compute_macd(data["close"])
    data["macd"] = macd_line
    data["macd_signal"] = signal_line

    last = data.iloc[-1]
    prev = data.iloc[-2] if len(data) >= 2 else last

    short_ma = float(last["sma_short"])
    long_ma = float(last["sma_long"])
    rsi_value = float(last["rsi"])
    macd_value = float(last["macd"])
    macd_signal_value = float(last["macd_signal"])
    close_price = float(last["close"])

    if pd.isna(short_ma) or pd.isna(long_ma):
        return SignalDecision("HOLD", "Waiting for enough data", 0.0, close_price)

    if short_ma > long_ma and rsi_value > 55 and macd_value > macd_signal_value:
        return SignalDecision("BUY", "Bullish trend confirmed by SMA, RSI, and MACD", 0.8, close_price)

    if short_ma < long_ma and rsi_value < 45 and macd_value < macd_signal_value:
        return SignalDecision("SELL", "Bearish trend confirmed by SMA, RSI, and MACD", 0.8, close_price)

    if prev["sma_short"] < prev["sma_long"] and short_ma > long_ma:
        return SignalDecision("BUY", "Golden cross observed", 0.7, close_price)

    if prev["sma_short"] > prev["sma_long"] and short_ma < long_ma:
        return SignalDecision("SELL", "Death cross observed", 0.7, close_price)

    return SignalDecision("HOLD", "Trend is neutral or inconsistent", 0.2, close_price)

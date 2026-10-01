from __future__ import annotations

from typing import Any

from .config import DEFAULT_CONFIG
from .data import generate_synthetic_market_data
from .strategy import generate_signal


def run_backtest(
    data: Any | None = None,
    initial_capital: float = DEFAULT_CONFIG.initial_capital,
    risk_per_trade: float = DEFAULT_CONFIG.risk_per_trade,
    max_position_size: float = DEFAULT_CONFIG.max_position_size,
    max_drain: float = DEFAULT_CONFIG.max_drawdown,
) -> dict:
    """Run a simple backtest over synthetic or provided market data."""
    market_data = data if data is not None else generate_synthetic_market_data(length=300)
    cash = initial_capital
    position = 0.0
    entry_price = 0.0
    trades = []
    equity_curve = [initial_capital]
    peak_equity = initial_capital
    max_drawdown = 0.0

    for idx, row in market_data.iterrows():
        history = market_data.iloc[: idx + 1].copy()
        signal = generate_signal(history)
        current_price = float(row["close"])

        if idx < 60:
            current_equity = cash + position * current_price
            peak_equity = max(peak_equity, current_equity)
            if peak_equity > 0:
                max_drawdown = max(max_drawdown, (peak_equity - current_equity) / peak_equity)
            equity_curve.append(current_equity)
            continue

        if signal.action == "BUY" and position <= 0:
            risk_budget = initial_capital * risk_per_trade
            stop_loss_pct = 0.02
            quantity = risk_budget / (current_price * stop_loss_pct)
            max_qty = (initial_capital * max_position_size) / current_price
            quantity = min(quantity, max_qty)
            if quantity > 0:
                cost = quantity * current_price
                if cash >= cost:
                    cash -= cost
                    position = quantity
                    entry_price = current_price
                    trades.append({"side": "BUY", "entry": current_price, "quantity": quantity})

        elif signal.action == "SELL" and position > 0:
            exit_value = position * current_price
            cash += exit_value
            pnl = (current_price - entry_price) * position
            trades[-1]["exit"] = current_price
            trades[-1]["pnl"] = pnl
            position = 0.0
            entry_price = 0.0

        current_equity = cash + position * current_price
        peak_equity = max(peak_equity, current_equity)
        if peak_equity > 0:
            max_drawdown = max(max_drawdown, (peak_equity - current_equity) / peak_equity)
        equity_curve.append(current_equity)

    # if position remains open, close it at the last price
    if position > 0 and entry_price > 0:
        last_close = float(market_data.iloc[-1]["close"])
        cash += position * last_close
        pnl = (last_close - entry_price) * position
        trades[-1]["exit"] = last_close
        trades[-1]["pnl"] = pnl
        position = 0.0
        entry_price = 0.0

    completed = [t for t in trades if "pnl" in t]
    win_count = sum(1 for t in completed if t["pnl"] > 0)
    total_pnl = sum(t["pnl"] for t in completed)
    final_equity = cash
    total_trades = len(completed)
    win_rate = (win_count / total_trades * 100.0) if total_trades else 0.0

    return {
        "total_trades": total_trades,
        "win_rate": win_rate,
        "total_pnl": total_pnl,
        "final_equity": final_equity,
        "max_drawdown": max_drawdown,
        "equity_curve": equity_curve,
        "trades": completed,
    }


def main() -> None:
    result = run_backtest()
    print("=== Backtest Summary ===")
    print(f"Total trades: {result['total_trades']}")
    print(f"Win rate: {result['win_rate']:.2f}%")
    print(f"Total PnL: {result['total_pnl']:.2f}")
    print(f"Final equity: {result['final_equity']:.2f}")
    print(f"Max drawdown: {result['max_drawdown']:.4f}")


if __name__ == "__main__":
    main()

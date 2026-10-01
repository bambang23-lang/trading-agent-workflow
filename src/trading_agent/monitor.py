from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TradeRecord:
    timestamp: str
    side: str
    entry_price: float
    exit_price: float | None = None
    quantity: float = 0.0
    pnl: float = 0.0


class PortfolioMonitor:
    def __init__(self, initial_capital: float):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.position = 0.0
        self.entry_price = None
        self.trade_history: list[TradeRecord] = []
        self.equity_curve: list[float] = [initial_capital]
        self.peak_equity = initial_capital
        self.max_drawdown = 0.0

    def open_position(self, order, timestamp: str):
        if order is None:
            return
        self.position = order.quantity
        self.entry_price = order.price
        self.cash -= order.notional
        self.trade_history.append(
            TradeRecord(timestamp=timestamp, side=order.side, entry_price=order.price, quantity=order.quantity)
        )

    def close_position(self, exit_price: float, timestamp: str):
        if self.position <= 0 or self.entry_price is None:
            return

        pnl = (exit_price - self.entry_price) * self.position
        self.cash += exit_price * self.position
        self.position = 0.0
        self.entry_price = None

        latest_trade = self.trade_history[-1]
        latest_trade.exit_price = exit_price
        latest_trade.pnl = pnl

        self.equity_curve.append(self.cash)
        self.update_drawdown()

    def update_drawdown(self):
        current_equity = self.cash + (self.position * (self.entry_price if self.entry_price else 0.0))
        self.peak_equity = max(self.peak_equity, current_equity)
        if self.peak_equity > 0:
            self.max_drawdown = max(self.max_drawdown, (self.peak_equity - current_equity) / self.peak_equity)

    def mark_to_market(self, price: float):
        if self.position > 0 and self.entry_price is not None:
            current_equity = self.cash + self.position * price
            self.peak_equity = max(self.peak_equity, current_equity)
            if self.peak_equity > 0:
                self.max_drawdown = max(self.max_drawdown, (self.peak_equity - current_equity) / self.peak_equity)

    def summary(self):
        realized_pnl = sum(t.pnl for t in self.trade_history if t.pnl is not None)
        completed_trades = [t for t in self.trade_history if t.exit_price is not None]
        wins = sum(1 for t in completed_trades if t.pnl > 0)
        win_rate = (wins / len(completed_trades) * 100) if completed_trades else 0.0
        final_equity = self.cash + (self.position * (self.entry_price if self.entry_price else 0.0))
        return {
            "total_trades": len(completed_trades),
            "win_rate": win_rate,
            "total_pnl": realized_pnl,
            "final_equity": final_equity,
            "max_drawdown": self.max_drawdown,
            "equity_curve": self.equity_curve,
        }

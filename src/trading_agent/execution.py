from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Order:
    side: str
    quantity: float
    price: float
    notional: float
    stop_loss: float
    take_profit: float


class ExecutionEngine:
    def __init__(self, risk_per_trade: float = 0.02, max_position_size: float = 0.4):
        self.risk_per_trade = risk_per_trade
        self.max_position_size = max_position_size

    def place_order(self, signal_action: str, current_price: float, equity: float) -> Order | None:
        if current_price <= 0 or equity <= 0:
            return None

        stop_loss_pct = 0.02

        if signal_action == "BUY":
            qty = (equity * self.risk_per_trade) / (current_price * stop_loss_pct)
            max_qty = (equity * self.max_position_size) / current_price
            qty = min(qty, max_qty)
            if qty <= 0:
                return None
            stop_loss = current_price * (1 - stop_loss_pct)
            take_profit = current_price * (1 + (2 * stop_loss_pct))
            return Order(
                side="BUY",
                quantity=qty,
                price=current_price,
                notional=qty * current_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
            )

        if signal_action == "SELL":
            qty = (equity * self.risk_per_trade) / (current_price * stop_loss_pct)
            max_qty = (equity * self.max_position_size) / current_price
            qty = min(qty, max_qty)
            if qty <= 0:
                return None
            stop_loss = current_price * (1 + stop_loss_pct)
            take_profit = current_price * (1 - (2 * stop_loss_pct))
            return Order(
                side="SELL",
                quantity=qty,
                price=current_price,
                notional=qty * current_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
            )

        return None

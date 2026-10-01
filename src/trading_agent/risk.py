from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskOutput:
    capital_risk: float
    stop_loss_pct: float
    position_size: float
    quantity: float


def position_size_from_risk(equity: float, risk_per_trade: float, stop_loss_pct: float, current_price: float, max_position_size: float) -> RiskOutput:
    if equity <= 0 or current_price <= 0:
        return RiskOutput(0.0, 0.0, 0.0, 0.0)

    capital_risk = equity * risk_per_trade
    stop_loss_pct = max(stop_loss_pct, 0.01)
    quantity = capital_risk / (current_price * stop_loss_pct)
    max_quantity = (equity * max_position_size) / current_price
    quantity = min(quantity, max_quantity)
    position_size = quantity * current_price

    return RiskOutput(
        capital_risk=capital_risk,
        stop_loss_pct=stop_loss_pct,
        position_size=position_size,
        quantity=quantity,
    )

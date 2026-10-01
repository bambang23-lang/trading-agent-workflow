from __future__ import annotations

from .config import DEFAULT_CONFIG
from .data import generate_synthetic_market_data
from .execution import ExecutionEngine, PortfolioMonitor
from .strategy import generate_signal


class TradingAgentPipeline:
    def __init__(self, config=DEFAULT_CONFIG):
        self.config = config
        self.market_data = generate_synthetic_market_data(length=300)
        self.execution_engine = ExecutionEngine(
            risk_per_trade=config.risk_per_trade,
            max_position_size=config.max_position_size,
        )
        self.monitor = PortfolioMonitor(initial_capital=config.initial_capital)
        self.trades = []

    def run(self):
        for idx, row in self.market_data.iterrows():
            history = self.market_data.iloc[: idx + 1].copy()
            signal = generate_signal(history)
            current_price = float(row["close"])

            if idx < 60:
                self.monitor.mark_to_market(current_price)
                continue

            if signal.action == "BUY" and self.monitor.position <= 0:
                order = self.execution_engine.place_order(signal.action, current_price, self.monitor.cash)
                if order is not None:
                    self.monitor.open_position(order, str(row["timestamp"]))
                    self.trades.append({"timestamp": row["timestamp"], "side": "BUY", "price": current_price})

            elif signal.action == "SELL" and self.monitor.position > 0:
                self.monitor.close_position(current_price, str(row["timestamp"]))
                self.trades.append({"timestamp": row["timestamp"], "side": "SELL", "price": current_price})

            self.monitor.mark_to_market(current_price)

        return self.monitor.summary()

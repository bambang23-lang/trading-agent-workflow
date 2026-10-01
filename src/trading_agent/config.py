from dataclasses import dataclass

INITIAL_CAPITAL = 100000.0
RISK_PER_TRADE = 0.02
MAX_POSITION_SIZE = 0.4
MAX_DRAWDOWN = 0.25

@dataclass(frozen=True)
class TradingConfig:
    initial_capital: float = INITIAL_CAPITAL
    risk_per_trade: float = RISK_PER_TRADE
    max_position_size: float = MAX_POSITION_SIZE
    max_drawdown: float = MAX_DRAWDOWN

DEFAULT_CONFIG = TradingConfig()

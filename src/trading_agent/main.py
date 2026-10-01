from __future__ import annotations

from .config import DEFAULT_CONFIG
from .pipeline import TradingAgentPipeline


def main() -> None:
    pipeline = TradingAgentPipeline(config=DEFAULT_CONFIG)
    summary = pipeline.run()

    print("=== Trading Agent Summary ===")
    print(f"Total trades: {summary['total_trades']}")
    print(f"Win rate: {summary['win_rate']:.2f}%")
    print(f"Total PnL: {summary['total_pnl']:.2f}")
    print(f"Final equity: {summary['final_equity']:.2f}")
    print(f"Max drawdown: {summary['max_drawdown']:.4f}")


if __name__ == "__main__":
    main()

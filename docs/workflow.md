# Trading Agent Workflow

This project demonstrates a clean architecture for a trading agent pipeline.

## Development notes

The system uses a modular approach so each component has a specific role:

- `data.py` builds synthetic market data
- `indicators.py` calculates technical indicators
- `strategy.py` defines buy/sell/hold logic
- `risk.py` limits position size and risk exposure
- `execution.py` simulates order execution
- `monitor.py` tracks equity, PnL, and drawdown
- `pipeline.py` coordinates the full workflow

## Recommended next phase

Replace synthetic data with live exchange data and update the execution engine to place real orders through broker APIs.

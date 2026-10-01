# Trading Agent Workflow

A practical and production-oriented trading agent project built from scratch. This repository implements a complete workflow from raw market data to signal generation, risk management, simulated execution, and portfolio monitoring.

## Why this project?

Many trading bot tutorials stop at a single indicator or a toy strategy. This project is different because it follows a realistic trading agent workflow:

1. Data acquisition
2. Data cleaning and validation
3. Feature engineering
4. Signal generation
5. Risk controls
6. Order simulation
7. Portfolio monitoring
8. Performance review and optimization
9. Backtest evaluation
10. Dashboard reporting
11. Exchange and ML extension points

## Project structure

```text
trading-agent-workflow/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── src/
│   └── trading_agent/
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       ├── data.py
│       ├── indicators.py
│       ├── strategy.py
│       ├── risk.py
│       ├── execution.py
│       ├── monitor.py
│       ├── pipeline.py
│       ├── backtest.py
│       ├── database.py
│       ├── exchange.py
│       ├── ml_signal.py
│       ├── dashboard.py
│       ├── run_dashboard.py
│       └── main.py
└── docs/
    └── workflow.md
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the project

### 1) Strategy pipeline

```bash
python -m trading_agent.main
```

### 2) Backtest runner

```bash
python -m trading_agent.backtest
```

### 3) Generate dashboard

```bash
PYTHONPATH=src python -m trading_agent.run_dashboard
```

Open the generated dashboard file in the `dashboard_data/` folder.

## Environment variables

Copy `.env.example` to `.env` and fill in your credentials for live execution.

```bash
cp .env.example .env
```

## What the workflow does

This project creates synthetic market data, calculates technical indicators, produces BUY/SELL/HOLD signals, applies risk rules, simulates order execution, and outputs a summary of portfolio metrics. It also supports:

- SQLite persistence
- backtested strategy evaluation
- ML-based signal ideas
- exchange client integration to Binance/Alpaca
- HTML dashboard output

## Production upgrade path

This project is intentionally modular so it can evolve into a live agent using:
- Binance or Coinbase APIs
- Alpaca or Interactive Brokers integration
- PostgreSQL for trade history
- Redis for event handling
- machine learning models for signal generation
- a backtesting engine for historical validation

## Workflow summary

Market data -> cleaning -> indicators -> strategy -> risk -> execution -> monitoring -> optimization -> dashboard

## License

MIT

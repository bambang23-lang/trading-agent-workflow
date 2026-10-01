from __future__ import annotations

import json
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


def get_env_or_default(name: str, default: str = "") -> str:
    import os
    return os.getenv(name, default)


ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_DIR = ROOT / "dashboard_data"


def ensure_dashboard_dir() -> Path:
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    return DASHBOARD_DIR


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


ENV = {
    "BINANCE_API_KEY": get_env_or_default("BINANCE_API_KEY"),
    "BINANCE_API_SECRET": get_env_or_default("BINANCE_API_SECRET"),
    "ALPACA_API_KEY": get_env_or_default("ALPACA_API_KEY"),
    "ALPACA_API_SECRET": get_env_or_default("ALPACA_API_SECRET"),
    "ALPACA_BASE_URL": get_env_or_default("ALPACA_BASE_URL", "https://paper-trading.alpaca.markets"),
    "TRADING_ENV": get_env_or_default("TRADING_ENV", "paper"),
}

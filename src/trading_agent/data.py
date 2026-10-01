from __future__ import annotations

from datetime import datetime, timedelta

import numpy as np
import pandas as pd


def generate_synthetic_market_data(
    length: int = 250,
    start_price: float = 100.0,
    drift: float = 0.0005,
    volatility: float = 0.012,
    seed: int = 42,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    closes = np.empty(length, dtype=float)
    closes[0] = start_price

    for idx in range(1, length):
        shock = rng.normal(drift, volatility)
        closes[idx] = max(1.0, closes[idx - 1] * (1 + shock))

    opens = np.empty(length, dtype=float)
    opens[0] = closes[0] * (1 + rng.normal(0.0, 0.002))
    opens[1:] = closes[:-1]

    highs = np.maximum(opens, closes) * (1 + np.abs(rng.normal(0.0, volatility * 0.8, size=length)))
    lows = np.minimum(opens, closes) * (1 - np.abs(rng.normal(0.0, volatility * 0.7, size=length)))
    volume = rng.integers(900, 2500, length)

    timestamps = pd.date_range(
        start=datetime.utcnow() - timedelta(days=length // 24),
        periods=length,
        freq="1h",
    )

    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": volume,
        }
    )
    return df

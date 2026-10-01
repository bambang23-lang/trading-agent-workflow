import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class MLSignalGenerator:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create features for ML model."""
        data = df.copy()

        # Price features
        data["returns"] = data["close"].pct_change()
        data["volatility"] = data["returns"].rolling(20).std()
        data["momentum"] = data["close"].diff()

        # Volume features
        data["volume_ma"] = data["volume"].rolling(20).mean()
        data["volume_ratio"] = data["volume"] / data["volume_ma"]

        # Technical indicators
        data["sma_20"] = data["close"].rolling(20).mean()
        data["sma_50"] = data["close"].rolling(50).mean()
        data["rsi"] = self.compute_rsi(data["close"])

        # High-low range
        data["hl_range"] = (data["high"] - data["low"]) / data["close"]
        data["oc_range"] = (data["close"] - data["open"]) / data["close"]

        return data.dropna()

    @staticmethod
    def compute_rsi(series: pd.Series, period: int = 14) -> pd.Series:
        """Compute RSI."""
        delta = series.diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
        rs = avg_gain / avg_loss.replace(0, np.nan)
        return (100 - (100 / (1 + rs))).fillna(50)

    def train(self, df: pd.DataFrame, lookback: int = 5):
        """Train the ML model on historical data."""
        data = self.prepare_features(df)

        # Create target: 1 if price goes up in next `lookback` periods, 0 otherwise
        data["target"] = (data["close"].shift(-lookback) > data["close"]).astype(int)
        data = data.dropna()

        feature_cols = ["returns", "volatility", "momentum", "volume_ratio", "sma_20", "sma_50", "rsi", "hl_range", "oc_range"]
        X = data[feature_cols].values
        y = data["target"].values

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True

    def predict(self, df: pd.DataFrame) -> str:
        """Predict signal: BUY, SELL, or HOLD."""
        if not self.is_trained:
            return "HOLD"

        data = self.prepare_features(df)
        if data.empty:
            return "HOLD"

        feature_cols = ["returns", "volatility", "momentum", "volume_ratio", "sma_20", "sma_50", "rsi", "hl_range", "oc_range"]
        X = data[feature_cols].iloc[-1:].values
        X_scaled = self.scaler.transform(X)
        prediction = self.model.predict(X_scaled)[0]
        confidence = self.model.predict_proba(X_scaled)[0][prediction]

        # Current RSI for additional context
        rsi = data["rsi"].iloc[-1]

        if prediction == 1 and confidence > 0.65 and rsi < 70:
            return "BUY"
        elif prediction == 0 and confidence > 0.65 and rsi > 30:
            return "SELL"
        else:
            return "HOLD"

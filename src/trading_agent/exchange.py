import os

import ccxt
import pandas as pd


class BinanceClient:
    def __init__(self, api_key: str = None, api_secret: str = None):
        self.api_key = api_key or os.getenv("BINANCE_API_KEY")
        self.api_secret = api_secret or os.getenv("BINANCE_API_SECRET")
        self.exchange = ccxt.binance({"apiKey": self.api_key, "secret": self.api_secret})

    def fetch_ohlcv(self, symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 100) -> pd.DataFrame:
        """Fetch OHLCV data from Binance."""
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(
                ohlcv,
                columns=["timestamp", "open", "high", "low", "close", "volume"],
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            return df
        except Exception as e:
            print(f"Error fetching data from Binance: {e}")
            return pd.DataFrame()

    def get_balance(self) -> dict:
        """Get account balance."""
        try:
            return self.exchange.fetch_balance()
        except Exception as e:
            print(f"Error fetching balance: {e}")
            return {}

    def place_market_order(self, symbol: str, side: str, amount: float) -> dict:
        """Place a market order."""
        try:
            order = self.exchange.create_market_order(symbol, side, amount)
            return order
        except Exception as e:
            print(f"Error placing order: {e}")
            return {}

    def place_limit_order(self, symbol: str, side: str, amount: float, price: float) -> dict:
        """Place a limit order."""
        try:
            order = self.exchange.create_limit_order(symbol, side, amount, price)
            return order
        except Exception as e:
            print(f"Error placing limit order: {e}")
            return {}


class AlpacaClient:
    def __init__(self, api_key: str = None, base_url: str = None):
        try:
            from alpaca.trading.client import TradingClient
            from alpaca.data.historical import StockHistoricalDataClient
            from alpaca.data.requests import StockBarsRequest
            from alpaca.data.timeframe import TimeFrame
        except ImportError:
            raise ImportError("Please install alpaca-trade-api: pip install alpaca-trade-api")

        self.api_key = api_key or os.getenv("ALPACA_API_KEY")
        self.base_url = base_url or os.getenv("ALPACA_BASE_URL", "https://paper-trading.alpaca.markets")
        self.trading_client = TradingClient(self.api_key, base_url=self.base_url)
        self.data_client = StockHistoricalDataClient(self.api_key, base_url=self.base_url)
        self.StockBarsRequest = StockBarsRequest
        self.TimeFrame = TimeFrame

    def fetch_bars(self, symbol: str, timeframe: str = "1H", limit: int = 100) -> pd.DataFrame:
        """Fetch historical bar data from Alpaca."""
        try:
            request = self.StockBarsRequest(
                symbol_or_symbols=[symbol],
                timeframe=self.TimeFrame[timeframe],
                limit=limit,
            )
            bars = self.data_client.get_stock_bars(request)
            df = pd.DataFrame(
                [
                    {
                        "timestamp": bar.timestamp,
                        "open": bar.open,
                        "high": bar.high,
                        "low": bar.low,
                        "close": bar.close,
                        "volume": bar.volume,
                    }
                    for bar in bars[symbol]
                ]
            )
            return df
        except Exception as e:
            print(f"Error fetching bars from Alpaca: {e}")
            return pd.DataFrame()

    def get_account(self) -> dict:
        """Get account details."""
        try:
            return self.trading_client.get_account().__dict__
        except Exception as e:
            print(f"Error fetching account: {e}")
            return {}

    def place_order(self, symbol: str, qty: float, side: str, order_type: str = "market", limit_price: float = None) -> dict:
        """Place an order."""
        try:
            from alpaca.trading.requests import MarketOrderRequest, LimitOrderRequest
            from alpaca.trading.enums import OrderSide, TimeInForce

            order_side = OrderSide.BUY if side.upper() == "BUY" else OrderSide.SELL

            if order_type.lower() == "limit" and limit_price:
                request = LimitOrderRequest(symbol=symbol, limit_price=limit_price, qty=qty, side=order_side, time_in_force=TimeInForce.DAY)
            else:
                request = MarketOrderRequest(symbol=symbol, qty=qty, side=order_side, time_in_force=TimeInForce.DAY)

            order = self.trading_client.submit_order(request)
            return order.__dict__
        except Exception as e:
            print(f"Error placing order: {e}")
            return {}

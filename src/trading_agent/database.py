import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("trading_agent.db")


class TradingDatabase:
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self.conn = None
        self.initialize()

    def initialize(self):
        """Create database and tables if they don't exist."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                side TEXT,
                entry_price REAL,
                exit_price REAL,
                quantity REAL,
                pnl REAL,
                status TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS portfolio (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                cash REAL,
                position REAL,
                total_equity REAL,
                peak_equity REAL,
                drawdown REAL
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME,
                action TEXT,
                price REAL,
                confidence REAL,
                reason TEXT
            )
        """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS backtest_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_timestamp DATETIME,
                initial_capital REAL,
                final_equity REAL,
                total_trades INTEGER,
                win_rate REAL,
                total_pnl REAL,
                max_drawdown REAL,
                sharpe_ratio REAL
            )
        """
        )

        self.conn.commit()

    def add_trade(self, timestamp: str, side: str, entry_price: float, quantity: float, exit_price: float = None, pnl: float = None, status: str = "OPEN"):
        """Record a trade."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO trades (timestamp, side, entry_price, exit_price, quantity, pnl, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (timestamp, side, entry_price, exit_price, quantity, pnl, status),
        )
        self.conn.commit()

    def close_trade(self, trade_id: int, exit_price: float, pnl: float):
        """Close an open trade."""
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE trades SET exit_price = ?, pnl = ?, status = ? WHERE id = ?",
            (exit_price, pnl, "CLOSED", trade_id),
        )
        self.conn.commit()

    def add_portfolio_snapshot(self, timestamp: str, cash: float, position: float, total_equity: float, peak_equity: float, drawdown: float):
        """Record portfolio state."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO portfolio (timestamp, cash, position, total_equity, peak_equity, drawdown) VALUES (?, ?, ?, ?, ?, ?)",
            (timestamp, cash, position, total_equity, peak_equity, drawdown),
        )
        self.conn.commit()

    def add_signal(self, timestamp: str, action: str, price: float, confidence: float, reason: str):
        """Record a signal."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO signals (timestamp, action, price, confidence, reason) VALUES (?, ?, ?, ?, ?)",
            (timestamp, action, price, confidence, reason),
        )
        self.conn.commit()

    def add_backtest_result(self, initial_capital: float, final_equity: float, total_trades: int, win_rate: float, total_pnl: float, max_drawdown: float, sharpe_ratio: float = 0.0):
        """Record backtest results."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO backtest_results (run_timestamp, initial_capital, final_equity, total_trades, win_rate, total_pnl, max_drawdown, sharpe_ratio) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (datetime.utcnow().isoformat(), initial_capital, final_equity, total_trades, win_rate, total_pnl, max_drawdown, sharpe_ratio),
        )
        self.conn.commit()

    def get_all_trades(self):
        """Fetch all trades."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM trades")
        return cursor.fetchall()

    def get_portfolio_history(self):
        """Fetch portfolio history."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM portfolio ORDER BY timestamp")
        return cursor.fetchall()

    def get_backtest_results(self):
        """Fetch recent backtest results."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM backtest_results ORDER BY run_timestamp DESC LIMIT 10")
        return cursor.fetchall()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

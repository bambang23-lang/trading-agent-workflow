import json
from datetime import datetime
from pathlib import Path

import pandas as pd


class DashboardData:
    def __init__(self, output_dir: str = "dashboard_data"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def save_portfolio_snapshot(self, timestamp: str, cash: float, position: float, total_equity: float, max_drawdown: float):
        """Save current portfolio state for dashboard."""
        data = {
            "timestamp": timestamp,
            "cash": round(cash, 2),
            "position": round(position, 4),
            "total_equity": round(total_equity, 2),
            "max_drawdown": round(max_drawdown, 4),
        }
        with open(self.output_dir / "portfolio.json", "w") as f:
            json.dump(data, f, indent=2)

    def save_trades_summary(self, trades: list):
        """Save trade summary for dashboard."""
        summary = {
            "total_trades": len(trades),
            "recent_trades": trades[-10:],  # Last 10 trades
        }
        with open(self.output_dir / "trades.json", "w") as f:
            json.dump(summary, f, indent=2, default=str)

    def save_equity_curve(self, equity_curve: list):
        """Save equity curve for charting."""
        data = {"equity_curve": [round(e, 2) for e in equity_curve]}
        with open(self.output_dir / "equity_curve.json", "w") as f:
            json.dump(data, f, indent=2)

    def save_performance_metrics(self, metrics: dict):
        """Save performance metrics."""
        with open(self.output_dir / "metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)

    def generate_html_dashboard(self, portfolio_data: dict, trades: list, equity_curve: list, metrics: dict) -> str:
        """Generate a simple HTML dashboard."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Trading Agent Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .card {{ background: white; padding: 20px; margin: 10px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metrics {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }}
        .metric {{ padding: 15px; background: #f9f9f9; border-left: 4px solid #007bff; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #333; }}
        .metric-label {{ font-size: 12px; color: #666; margin-top: 5px; }}
        h1 {{ color: #333; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #007bff; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Trading Agent Dashboard</h1>
        <p>Last updated: {datetime.utcnow().isoformat()}</p>

        <div class="card">
            <h2>Portfolio Metrics</h2>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">${portfolio_data.get('total_equity', 0):,.2f}</div>
                    <div class="metric-label">Total Equity</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${portfolio_data.get('cash', 0):,.2f}</div>
                    <div class="metric-label">Cash</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{metrics.get('win_rate', 0):.2f}%</div>
                    <div class="metric-label">Win Rate</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{metrics.get('max_drawdown', 0):.4f}</div>
                    <div class="metric-label">Max Drawdown</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>Equity Curve</h2>
            <canvas id="equityChart"></canvas>
        </div>

        <div class="card">
            <h2>Recent Trades ({len(trades)})</h2>
            <table>
                <tr>
                    <th>Side</th>
                    <th>Entry Price</th>
                    <th>Exit Price</th>
                    <th>PnL</th>
                    <th>Status</th>
                </tr>
        """

        for trade in trades[-20:]:  # Last 20 trades
            pnl = trade.get("pnl", "N/A")
            pnl_color = "green" if isinstance(pnl, float) and pnl > 0 else "red"
            html += f"""
                <tr>
                    <td>{trade.get('side', 'N/A')}</td>
                    <td>${trade.get('entry', 0):.2f}</td>
                    <td>${trade.get('exit', 'N/A')}</td>
                    <td><span style="color: {pnl_color}">{pnl if isinstance(pnl, str) else f'${pnl:.2f}'}</span></td>
                    <td>Closed</td>
                </tr>
            """

        html += f"""
            </table>
        </div>
    </div>

    <script>
        const ctx = document.getElementById('equityChart').getContext('2d');
        new Chart(ctx, {{
            type: 'line',
            data: {{
                labels: Array.from({{length: {len(equity_curve)}}}, (_, i) => i),
                datasets: [{{
                    label: 'Equity',
                    data: {equity_curve},
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    tension: 0.1,
                    fill: true
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        display: true,
                        position: 'top'
                    }}
                }},
                scales: {{
                    y: {{
                        beginAtZero: false
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
        """
        return html

from __future__ import annotations

from pathlib import Path

from .backtest import run_backtest
from .dashboard import DashboardData


def main() -> None:
    result = run_backtest()
    dashboard = DashboardData(output_dir="dashboard_data")
    dashboard.save_equity_curve(result["equity_curve"])
    dashboard.save_trades_summary(result["trades"])
    dashboard.save_performance_metrics(
        {
            "total_trades": result["total_trades"],
            "win_rate": result["win_rate"],
            "total_pnl": result["total_pnl"],
            "final_equity": result["final_equity"],
            "max_drawdown": result["max_drawdown"],
        }
    )

    portfolio_data = {
        "cash": result["final_equity"],
        "position": 0.0,
        "total_equity": result["final_equity"],
    }
    html = dashboard.generate_html_dashboard(
        portfolio_data=portfolio_data,
        trades=result["trades"],
        equity_curve=result["equity_curve"],
        metrics={
            "win_rate": result["win_rate"],
            "max_drawdown": result["max_drawdown"],
        },
    )

    output_path = Path("dashboard_data/index.html")
    output_path.write_text(html, encoding="utf-8")
    print(f"Dashboard generated: {output_path.resolve()}")


if __name__ == "__main__":
    main()

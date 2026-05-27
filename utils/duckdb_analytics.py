import duckdb
import pandas as pd
from typing import Optional


class DuckDBAnalytics:

    def __init__(self):
        self.con = duckdb.connect()

    def load_data(self):
        self.sales = pd.read_csv("data/sales.csv")
        self.hr = pd.read_csv("data/hr.csv")
        self.finance = pd.read_csv("data/finance.csv")
        self.production = pd.read_json("data/production.json")

        for df in [self.sales, self.hr, self.finance, self.production]:
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"]).dt.date

        self.con.register("sales", self.sales)
        self.con.register("hr", self.hr)
        self.con.register("finance", self.finance)
        self.con.register("production", self.production)

    def _date_filter(self, col: str, start_date: Optional[str], end_date: Optional[str]) -> str:
        parts = []
        if start_date:
            parts.append(f"CAST({col} AS DATE) >= DATE '{start_date}'")
        if end_date:
            parts.append(f"CAST({col} AS DATE) <= DATE '{end_date}'")
        return (" AND " + " AND ".join(parts)) if parts else ""

    def calculate_profit_loss(self, start_date=None, end_date=None) -> dict:
        self.load_data()
        sf = self._date_filter("date", start_date, end_date)

        total_income    = self.con.execute(f"SELECT COALESCE(SUM(amount), 0) FROM sales WHERE 1=1{sf}").fetchone()[0]
        hr_cost         = self.con.execute(f"SELECT COALESCE(SUM(salary), 0) FROM hr WHERE 1=1{sf}").fetchone()[0]
        finance_cost    = self.con.execute(f"SELECT COALESCE(SUM(amount), 0) FROM finance WHERE 1=1{sf}").fetchone()[0]
        production_cost = self.con.execute(f"SELECT COALESCE(SUM(cost), 0) FROM production WHERE 1=1{sf}").fetchone()[0]

        total_expenses = hr_cost + finance_cost + production_cost
        profit_loss    = total_income - total_expenses

        return {
            "total_income":     float(total_income),
            "total_expenses":   float(total_expenses),
            "profit_loss":      float(profit_loss),
            "hr_cost":          float(hr_cost),
            "finance_cost":     float(finance_cost),
            "production_cost":  float(production_cost),
            "status":           "Profit" if profit_loss >= 0 else "Loss",
            "period":           {"start": start_date, "end": end_date},
        }

    def get_department_breakdown(self, start_date=None, end_date=None) -> list:
        self.load_data()
        sf = self._date_filter("date", start_date, end_date)

        sales_val      = self.con.execute(f"SELECT COALESCE(SUM(amount), 0) FROM sales WHERE 1=1{sf}").fetchone()[0]
        hr_val         = self.con.execute(f"SELECT COALESCE(SUM(salary), 0) FROM hr WHERE 1=1{sf}").fetchone()[0]
        finance_val    = self.con.execute(f"SELECT COALESCE(SUM(amount), 0) FROM finance WHERE 1=1{sf}").fetchone()[0]
        production_val = self.con.execute(f"SELECT COALESCE(SUM(cost), 0) FROM production WHERE 1=1{sf}").fetchone()[0]

        return [
            {"department": "Sales",      "value":  float(sales_val),      "type": "income"},
            {"department": "HR",         "value": -float(hr_val),          "type": "expense"},
            {"department": "Finance",    "value": -float(finance_val),     "type": "expense"},
            {"department": "Production", "value": -float(production_val),  "type": "expense"},
        ]

    def get_expenses_by_period(self, start_date=None, end_date=None, group_by="day") -> list:
        self.load_data()

        hr_cols    = self.hr.columns.tolist()
        fin_cols   = self.finance.columns.tolist()
        prod_cols  = self.production.columns.tolist()
        sales_cols = self.sales.columns.tolist()

        if group_by == "month":
            trunc = "STRFTIME('%Y-%m', CAST(date AS DATE))"
        elif group_by == "week":
            trunc = "STRFTIME('%Y-W%W', CAST(date AS DATE))"
        else:
            trunc = "STRFTIME('%Y-%m-%d', CAST(date AS DATE))"

        def make_query(table, val_col, has_date):
            if not has_date:
                return f"SELECT 'no-date' AS period, COALESCE(SUM({val_col}), 0) AS val FROM {table}"
            sf = self._date_filter("date", start_date, end_date)
            return f"SELECT {trunc} AS period, COALESCE(SUM({val_col}), 0) AS val FROM {table} WHERE 1=1{sf} GROUP BY period"

        hr_q    = make_query("hr",         "salary", "date" in hr_cols)
        fin_q   = make_query("finance",    "amount", "date" in fin_cols)
        prod_q  = make_query("production", "cost",   "date" in prod_cols)
        sales_q = make_query("sales",      "amount", "date" in sales_cols)

        combined_q = f"""
            WITH all_data AS (
                SELECT period, val AS expense, 0 AS income FROM ({hr_q}) hr
                UNION ALL
                SELECT period, val AS expense, 0 AS income FROM ({fin_q}) fin
                UNION ALL
                SELECT period, val AS expense, 0 AS income FROM ({prod_q}) prod
                UNION ALL
                SELECT period, 0 AS expense, val AS income FROM ({sales_q}) sales
            )
            SELECT
                period,
                SUM(expense)               AS total_expense,
                SUM(income)                AS total_income,
                SUM(income) - SUM(expense) AS net
            FROM all_data
            GROUP BY period
            ORDER BY period
        """

        rows = self.con.execute(combined_q).fetchall()
        return [
            {
                "period":        r[0],
                "total_expense": float(r[1]),
                "total_income":  float(r[2]),
                "net":           float(r[3]),
            }
            for r in rows
        ]

    def get_stats(self, start_date=None, end_date=None) -> dict:
        self.load_data()
        sf = self._date_filter("date", start_date, end_date)

        sales_count = self.con.execute(f"SELECT COUNT(*) FROM sales WHERE 1=1{sf}").fetchone()[0]
        hr_count    = self.con.execute(f"SELECT COUNT(*) FROM hr WHERE 1=1{sf}").fetchone()[0]
        avg_sale    = self.con.execute(f"SELECT COALESCE(AVG(amount), 0) FROM sales WHERE 1=1{sf}").fetchone()[0]
        top_region  = self.con.execute(
            f"SELECT region, SUM(amount) AS total FROM sales WHERE 1=1{sf} GROUP BY region ORDER BY total DESC LIMIT 1"
        ).fetchone()

        return {
            "sales_transactions":  int(sales_count),
            "hr_records":          int(hr_count),
            "avg_sale_value":      float(avg_sale),
            "top_region":          top_region[0] if top_region else None,
            "top_region_revenue":  float(top_region[1]) if top_region else 0,
        }
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import date

from utils.duckdb_analytics import DuckDBAnalytics
from utils.ai_trends import generate_ai_insight, generate_period_insight

app = FastAPI(title="Financial Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Analytics API Running"}


@app.get("/api/summary")
def summary(
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD"),
):
    analytics = DuckDBAnalytics()
    data = analytics.calculate_profit_loss(start_date=start_date, end_date=end_date)
    return data


@app.get("/api/department-breakdown")
def breakdown(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    analytics = DuckDBAnalytics()
    return analytics.get_department_breakdown(start_date=start_date, end_date=end_date)


@app.get("/api/expenses-by-period")
def expenses_by_period(
    start_date: Optional[str] = Query(None, description="Start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="End date YYYY-MM-DD"),
    group_by: str = Query("day", description="Group by: day | week | month"),
):
    analytics = DuckDBAnalytics()
    return analytics.get_expenses_by_period(
        start_date=start_date, end_date=end_date, group_by=group_by
    )


@app.get("/api/stats")
def stats(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    analytics = DuckDBAnalytics()
    return analytics.get_stats(start_date=start_date, end_date=end_date)


@app.get("/api/ai-summary")
def ai_summary(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
):
    analytics = DuckDBAnalytics()
    summary_data = analytics.calculate_profit_loss(start_date=start_date, end_date=end_date)
    dept_data = analytics.get_department_breakdown(start_date=start_date, end_date=end_date)
    period_expenses = analytics.get_expenses_by_period(
        start_date=start_date, end_date=end_date, group_by="day"
    )
    return generate_ai_insight(summary_data, dept_data, period_expenses, start_date, end_date)


@app.get("/api/ai-period-analysis")
def ai_period_analysis(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    question: Optional[str] = Query(None, description="Natural language question about expenses"),
):
    analytics = DuckDBAnalytics()
    period_data = analytics.get_expenses_by_period(
        start_date=start_date, end_date=end_date, group_by="day"
    )
    dept_data = analytics.get_department_breakdown(start_date=start_date, end_date=end_date)
    summary_data = analytics.calculate_profit_loss(start_date=start_date, end_date=end_date)
    return generate_period_insight(summary_data, dept_data, period_data, question, start_date, end_date)
import os
import json
from groq import Groq
from typing import Optional

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def _call_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def generate_ai_insight(summary, dept_data, period_expenses, start_date=None, end_date=None):
    period_str = ""
    if start_date and end_date:
        period_str = f" for {start_date} to {end_date}"

    prompt = f"""You are a concise financial analyst. Give a 2-3 sentence business insight with a specific action. Never say 'Based on'. No bullet points.

Financial summary{period_str}:
- Income: ${summary['total_income']:,.0f}
- Expenses: ${summary['total_expenses']:,.0f}
- Profit/Loss: ${summary['profit_loss']:,.0f} ({summary['status']})
- HR: ${summary['hr_cost']:,.0f}, Finance: ${summary['finance_cost']:,.0f}, Production: ${summary['production_cost']:,.0f}

Department: {json.dumps(dept_data)}
Recent trend: {json.dumps(period_expenses[-7:] if period_expenses else [])}"""

    try:
        return {"ai_insight": _call_groq(prompt)}
    except Exception as e:
        return {"ai_insight": f"AI unavailable: {str(e)}"}


def generate_period_insight(summary, dept_data, period_data, question=None, start_date=None, end_date=None):
    period_str = f"{start_date} to {end_date}" if start_date and end_date else "all data"
    user_question = question or "Summarize expense patterns and highlight anomalies."

    prompt = f"""You are a financial data analyst. Answer in under 4 sentences with specific dollar amounts.

Period: {period_str}
Income: ${summary['total_income']:,.0f} | Expenses: ${summary['total_expenses']:,.0f} | Net: ${summary['profit_loss']:,.0f}
HR: ${summary['hr_cost']:,.0f} | Finance: ${summary['finance_cost']:,.0f} | Production: ${summary['production_cost']:,.0f}

Daily data: {json.dumps(period_data)}

Question: {user_question}"""

    try:
        return {
            "question": user_question,
            "answer": _call_groq(prompt),
            "period": {"start": start_date, "end": end_date},
            "data_summary": {
                "total_expense": summary["total_expenses"],
                "total_income": summary["total_income"],
                "net": summary["profit_loss"],
            }
        }
    except Exception as e:
        return {
            "question": user_question,
            "answer": f"AI unavailable: {str(e)}",
            "period": {"start": start_date, "end": end_date},
            "data_summary": {}
        }
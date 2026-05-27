## Live Financial Analytics Dashboard

Real-time business analytics dashboard with AI-powered insights.

### Stack
- FastAPI — REST API backend
- DuckDB — in-memory SQL analytics on live CSV/JSON data
- Groq API (LLaMA 3.3 70B) — AI insights and natural language Q&A
- Chart.js — interactive charts
- Faker — realistic data generation

### Features
- Live data generation every 5 seconds
- Date range filtering (day/week/month)
- Department performance breakdown
- AI business insight on every refresh
- Ask questions about your data in plain English

### Run
Terminal 1: python generate.py
Terminal 2: GROQ_API_KEY=your-key uvicorn main:app --host 127.0.0.1 --port 8000
Terminal 3: python -m http.server 3000

Open: http://localhost:3000/dashboard.html

Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

 License

MIT License - see [LICENSE](LICENSE) file for details

  Author
 
Chandra K
- GitHub: [@Chandra20052025(https://github.com/Chandra20052025)
- LinkedIn: https://www.linkedin.com/in/chandra-k-68b867315/
⭐ If you found this helpful, please star this repository!

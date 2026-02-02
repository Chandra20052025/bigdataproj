from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.spark_analytics import SparkAnalytics

app = FastAPI(title="PySpark Company Analytics API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Spark Analytics
analytics = None

def get_analytics():
    """Get or create analytics instance"""
    global analytics
    if analytics is None:
        analytics = SparkAnalytics()
        analytics.load_all_data()
    return analytics

@app.get("/")
def root():
    return {"message": "PySpark Company Analytics API", "status": "running"}

@app.get("/api/summary")
def get_summary():
    """Get profit/loss summary"""
    try:
        a = get_analytics()
        return a.calculate_profit_loss()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/api/department-breakdown")
def get_department_breakdown():
    """Get department-wise breakdown"""
    try:
        a = get_analytics()
        return a.get_department_breakdown()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.get("/api/stats")
def get_stats():
    """Get detailed statistics"""
    try:
        a = get_analytics()
        return a.get_detailed_stats()
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.post("/api/refresh")
def refresh_data():
    """Reload data from files"""
    try:
        global analytics
        if analytics:
            analytics.stop()
        analytics = SparkAnalytics()
        analytics.load_all_data()
        return {"status": "success", "message": "Data refreshed successfully"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )

@app.on_event("shutdown")
def shutdown_event():
    """Stop Spark when API shuts down"""
    global analytics
    if analytics:
        analytics.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)    
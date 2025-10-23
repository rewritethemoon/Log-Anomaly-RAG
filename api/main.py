# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sys
from pathlib import Path
import uvicorn  # THÊM DÒNG NÀY

# Thêm root
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from src.inference import analyze_log

app = FastAPI(
    title="Log Anomaly Detection & RAG Assistant",
    description="Detect anomalies and explain logs using ML + RAG",
    version="1.0"
)

class LogInput(BaseModel):
    Message: str
    Latency: float = 0.0
    MsgLength: int = 0
    Hour: int = 0
    DayOfWeek: int = 0
    Component: str = "UNKNOWN"
    Keywords: str = ""

@app.get("/")
def home():
    return {"status": "API is running!", "docs": "http://127.0.0.1:8001/docs"}

@app.post("/analyze")
def analyze_log_api(input: LogInput):
    try:
        result = analyze_log(input.dict())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# CHẠY API TRÊN PORT 8001 (TRÁNH XUNG ĐỘ)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
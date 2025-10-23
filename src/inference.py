# src/inference.py
from pathlib import Path
import sys

# Thêm root vào path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT))

from src.rag_pipeline import RAGPipeline  # ĐÚNG

DATA_PATH = ROOT / "data" / "processed" / "BGL_preprocessed.csv"
rag = RAGPipeline(DATA_PATH)
rag.load_faiss()  # Sẽ load index đã tạo

def analyze_log(log_dict):
    pred = rag.predict_anomaly([log_dict])
    is_anomaly = bool(pred[0])
    explanation = rag.explain_log(log_dict['Message'])
    return {
        "anomaly": is_anomaly,
        "explanation": explanation
    }

# TEST
if __name__ == "__main__":
    sample = {
        "Message": "instruction cache parity error corrected",
        "Latency": 0.1,
        "MsgLength": 40,
        "Hour": 15,
        "DayOfWeek": 4,
        "Component": "RAS",
        "Keywords": "corrected parity cache error"
    }
    result = analyze_log(sample)
    print("\nKẾT QUẢ PHÂN TÍCH:")
    print(result)
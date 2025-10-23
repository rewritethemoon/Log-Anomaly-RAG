# app.py
import streamlit as st
import requests
import sys
from pathlib import Path

# Thêm root vào sys.path
ROOT = Path(__file__).parent
sys.path.append(str(ROOT))

# app.py → DÒNG 12
API_URL = "http://127.0.0.1:8001/analyze"

# --- GIAO DIỆN ---
st.set_page_config(page_title="Log RAG Assistant", layout="centered")
st.title("Log Anomaly Detection with RAG")
st.markdown("### Nhập log → Nhận cảnh báo + giải thích")

with st.form("log_form"):
    message = st.text_area(
        "Log Message",
        value="instruction cache parity error corrected",
        height=100
    )
    
    col1, col2 = st.columns(2)
    with col1:
        latency = st.slider("Latency (s)", 0.0, 10.0, 0.1)
        hour = st.slider("Hour (0-23)", 0, 23, 15)
    with col2:
        msglen = st.slider("Message Length", 10, 200, 40)
        day = st.selectbox("Day of Week", [0,1,2,3,4,5,6], index=4)
    
    component = st.text_input("Component", "RAS")
    keywords = st.text_input("Keywords", "corrected parity cache error")
    
    submitted = st.form_submit_button("Phân tích Log")

if submitted:
    payload = {
        "Message": message,
        "Latency": latency,
        "MsgLength": msglen,
        "Hour": hour,
        "DayOfWeek": day,
        "Component": component,
        "Keywords": keywords
    }
    
    with st.spinner("Đang phân tích..."):
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                result = response.json()
                if result['anomaly']:
                    st.error("**PHÁT HIỆN ANOMALY**")
                else:
                    st.success("**Log BÌNH THƯỜNG**")
                st.info(f"**Giải thích:** {result['explanation']}")
            else:
                st.error(f"API lỗi: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Không kết nối được API. Hãy chạy lệnh sau trong terminal:\n```python api/main.py```")
        except Exception as e:
            st.error(f"Lỗi: {e}")
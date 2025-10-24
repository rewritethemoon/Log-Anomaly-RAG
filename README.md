# Log Anomaly Detection with RAG

**Grab Intern Project 2025**  
*Unsupervised Machine Learning + Retrieval-Augmented Generation for Intelligent Log Analysis*

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](http://localhost:8501)  
[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)  
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)  
[![GitHub Issues](https://img.shields.io/github/issues/rewritethemoon/Log-Anomaly-RAG)](https://github.com/rewritethemoon/Log-Anomaly-RAG/issues)  

---

## Overview

This project is an intelligent log analysis system developed for the Grab 2025 Intern Program. It combines **Unsupervised Machine Learning (Isolation Forest)** and **Retrieval-Augmented Generation (RAG)** using a pre-trained language model (`flan-t5-base`) to detect anomalies in system logs and provide human-readable explanations. The system includes a **FastAPI backend**, a **Streamlit frontend**, and supports multiple deployment options.

- **ML Performance**: F1-score = 0.395, Recall = 100%
- **RAG**: FAISS index with `all-MiniLM-L6-v2` embeddings
- **Deployment**: Local 1-click run, Docker, and standalone `.exe`

---

## Features

- **Anomaly Detection**: Identifies abnormal logs using Isolation Forest.
- **Explanation Generation**: Uses RAG to explain logs based on historical context.
- **Real-time API**: FastAPI endpoint for log analysis.
- **Interactive Demo**: Streamlit UI for easy testing.
- **Flexible Deployment**: Run locally, on servers, or on any Windows PC without Python.

---

## Quick Start (1-Click Run)
For a seamless experience on Windows:

1. Download the repository:
   ```bash
   git clone https://github.com/rewritethemoon/Log-Anomaly-RAG.git
   cd Log-Anomaly-RAG
   ```
2. Download required models and data:
   ## Download Models and Data
   Download the required models and data here: [models_data.zip](https://drive.google.com/uc?export=download&id=1k72zENgTDKA87pU4tPt3uQuqVEifkN2-)
3. Extract the zip file:
   ```bash
   unzip models_data.zip
   ```
4. Run the system with a single click:
   ```bash
   double-click run.bat
   ```
5. Open your browser at: http://localhost:8501
   Note: Ensure Python 3.10+ is installed. The script will handle dependencies automatically.


Project Structure
textLog-Anomaly-RAG/
├── run.bat              # 1-click run script
├── api/                 # FastAPI backend
│   └── main.py          # API endpoint
├── app.py               # Streamlit frontend
├── src/                 # Core logic (RAG pipeline, ML)
├── deploy/              # Docker configuration
│   ├── Dockerfile
│   └── docker-compose.yml
├── standalone/          # Standalone .exe file
│   └── LogRAG_Assistant.exe
├── README.md            # This file
├── LICENSE              # MIT License
└── .gitignore           # Ignore large files and temp data

Installation
Prerequisites

Python 3.10+
Git (for cloning)
Docker (optional, for server deployment)

Dependencies
All dependencies are listed in requirements.txt. The run.bat script will install them automatically.
txtfastapi
uvicorn
streamlit
pandas
numpy
scikit-learn
joblib
faiss-cpu
sentence-transformers
transformers
torch

Deployment Options
1. Local Development (1-Click)

Use run.bat as described above.

2. Docker Deployment
For server deployment:
bashdocker-compose up --build

Access the demo at: http://your-server-ip:8501
Access the API at: http://your-server-ip:8001/docs

3. Standalone Execution (No Python Required)

Copy standalone/LogRAG_Assistant.exe to any Windows PC.
Double-click to run → Browser opens automatically.


Results





















MetricValueF1-Score (Anomaly)0.395Recall100%Prophet MAE1070

Explanation Example: "Auto-corrected, no action needed" for normal logs.


How It Works

Data Preprocessing: Loads and cleans log data from BGL_preprocessed.csv.
ML Model: Isolation Forest detects anomalies with high recall.
RAG Pipeline: FAISS retrieves similar logs, and flan-t5-base generates explanations.
API: FastAPI serves predictions and explanations.
UI: Streamlit provides an interactive interface.


Contributing
Feel free to open issues or submit pull requests!

Issues: https://github.com/rewritethemoon/Log-Anomaly-RAG/issues
Fork: Clone and improve the project.


License
This project is licensed under the MIT License.

Author

Name: [Your Name]
GitHub: rewritethemoon
LinkedIn: [linkedin.com/in/your-profile] (optional)


Acknowledgments

Thanks to the Grab Intern Program 2025 for the opportunity.
Inspired by xAI's Grok and Hugging Face's open-source models.

text---

# HƯỚNG DẪN SỬ DỤNG

1. **Sao chép nội dung trên** vào file `README.md` trong thư mục dự án của bạn (`C:\Users\Admin\Intelligent-Log-Analysis-and-Anomaly-Detection-Assistant-using-RAG-and-LLMs\README.md`).
2. **Thay link Google Drive**: Trong phần "Download required models and data", thay `https://drive.google.com/file/d/ABC123/view?usp=sharing` bằng link thực tế của bạn sau khi upload `models_data.zip`.
3. **Commit và push**:
   ```bash
   git add README.md
   git commit -m "docs: update README with professional content"
   git push

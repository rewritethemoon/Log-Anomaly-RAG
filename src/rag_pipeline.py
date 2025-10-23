# src/rag_pipeline.py
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
import faiss
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import torch

class RAGPipeline:
    def __init__(self, data_path, model_dir="models"):
        self.data_path = Path(data_path)
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        # Load data
        self.df = pd.read_csv(self.data_path, low_memory=False)
        self.df['Timestamp'] = pd.to_datetime(self.df['Timestamp'], errors='coerce')
        self.df['Anomaly_GT'] = (self.df['Label'] != '-').astype(int)
        
        # Load ML model
        self.preprocessor = joblib.load(self.model_dir / "preprocessor_clean.pkl")
        self.ml_model = joblib.load(self.model_dir / "isolation_forest_clean.pkl")
        
        # Embedding model
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        
        # LLM
        self.llm = pipeline(
        "text2text-generation",
        model="google/flan-t5-base",   
        tokenizer="google/flan-t5-base",
        max_length=256,
        temperature=0.3,
        do_sample=True,
        device=-1
        )
        
        # FAISS index
        self.index = None
        self.texts = None
        self.metadatas = None
        
    def build_faiss(self):
        print("Building FAISS index...")
        texts = self.df['Message'].fillna("").tolist()
        embeddings = self.embedder.encode(texts, show_progress_bar=True, batch_size=64)
        
        # FAISS
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype('float32'))
        
        self.texts = texts
        self.metadatas = self.df[['Timestamp', 'Node', 'Component', 'Severity']].to_dict('records')
        
        # Save
        faiss.write_index(self.index, str(self.model_dir / "faiss.index"))
        pd.DataFrame({"text": texts}).to_csv(self.model_dir / "faiss_texts.csv", index=False)
        joblib.dump(self.metadatas, self.model_dir / "faiss_metadata.pkl")
        print("FAISS index saved.")
        
    def load_faiss(self):
        index_path = self.model_dir / "faiss.index"
        if index_path.exists():
            self.index = faiss.read_index(str(index_path))
            self.texts = pd.read_csv(self.model_dir / "faiss_texts.csv")['text'].tolist()
            self.metadatas = joblib.load(self.model_dir / "faiss_metadata.pkl")
            print("FAISS loaded.")
        else:
            self.build_faiss()
    
    def retrieve(self, query, k=3):
        query_emb = self.embedder.encode([query])
        D, I = self.index.search(query_emb.astype('float32'), k)
        results = []
        for i, idx in enumerate(I[0]):
            if idx != -1:
                results.append({
                    "text": self.texts[idx],
                    "metadata": self.metadatas[idx],
                    "distance": D[0][i]
                })
        return results
    
    def predict_anomaly(self, logs):
        df_temp = pd.DataFrame(logs)
        required = ['Latency','MsgLength','Hour','DayOfWeek','Component','Keywords']
        X = self.preprocessor.transform(df_temp[required])
        pred = self.ml_model.predict(X)
        return np.where(pred == 1, 0, 1)
    
    def explain_log(self, message):
        if self.index is None:
            self.load_faiss()
        
        # Retrieve
        docs = self.retrieve(message, k=3)
        context = "\n".join([f"Log {i+1}: {d['text']}" for i, d in enumerate(docs)])
        
        # Prompt
        prompt = f"""
        You are a log analysis expert. Use the context below to explain this log:
        
        LOG: {message}
        
        CONTEXT:
        {context}
        
        Explain in 1-2 sentences. If anomaly, say why. If normal, say it's expected.
        """
        
        # Generate
        result = self.llm(prompt, max_length=150)[0]['generated_text']
        return result.strip()
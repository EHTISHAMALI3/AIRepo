from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="Toxic Comment Classifier API")
# ✅ Enable CORS for Angular frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:4200"],  # safer than ["*"]
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# Serve static frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://127.0.0.1:8000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_index():
    return FileResponse(os.path.join("static", "index.html"))
class Comment(BaseModel):
    text: str

# Load pipeline (model already includes TF-IDF)
MODEL_PATH = "models/tfidf_logreg.pkl"

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Model not found. Please train it first.")

# Load the full pipeline
model = joblib.load(MODEL_PATH)

@app.get("/")
def root():
    return {"message": "✅ Toxic Comment Classifier API is running!"}

@app.post("/predict")
def predict(comment: Comment):
    text = [comment.text]
    # 👇 No need to vectorize again, pipeline handles it
    prediction = model.predict(text)[0]
    probability = model.predict_proba(text)[0][1]

    return {
        "text": comment.text,
        "is_toxic": bool(prediction),
        "confidence": round(float(probability), 3)
    }

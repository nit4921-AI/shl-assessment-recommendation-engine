from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from .recommender import recommend_assessments

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"
INDEX_HTML = FRONTEND_DIR / "index.html"

app = FastAPI(title="SHL Assessment Recommendation Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)

# serve all frontend assets under /static
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

class QueryRequest(BaseModel):
  query: str
  top_k: int | None = None
  balance: bool | None = None

@app.get("/health")
def health():
  return {"status": "ok"}

@app.post("/recommend")
def recommend(req: QueryRequest):
  try:
    from .recommender import recommend_assessments
    top_k = req.top_k or 10
    balance = True if req.balance is None else req.balance
    items = recommend_assessments(req.query, top_k=top_k, balance_by_type=balance)
    return {"query": req.query, "recommendations": items}
  except Exception as e:
    raise HTTPException(status_code=400, detail=f"Recommendation error: {e}")

@app.get("/")
def root():
  if not INDEX_HTML.exists():
    raise HTTPException(status_code=404, detail="index.html not found")
  return FileResponse(str(INDEX_HTML))

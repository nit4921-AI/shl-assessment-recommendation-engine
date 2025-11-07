import os
from typing import List, Dict
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# ---- paths ----
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "shl_catalog.csv")

# ---- globals ----
_model = None
_catalog_df = None
_catalog_emb = None

# ---- helpers ----
def _load_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def _guess_test_type(name: str, url: str, desc: str) -> str:
    """
    Best-effort K/P guess when 'Test Type' column is missing.
    K = knowledge/skills (tech/content)
    P = personality/behavior
    """
    text = f"{name} {url} {desc}".lower()
    p_hits = [
        "personality", "behaviour", "behavior", "collaboration", "teamwork",
        "leadership", "work style", "communication", "motivation",
        "judgement", "judgment", "resilience", "culture", "sjt"
    ]
    k_hits = [
        "java", ".net", "python", "sql", "javascript", "angular", "react",
        "aws", "hadoop", "data", "coding", "test", "analysis", "numerical",
        "verbal", "aptitude", "reasoning", "mvc", "wpf", "xaml", "android"
    ]
    if any(w in text for w in p_hits):
        return "P"
    if any(w in text for w in k_hits):
        return "K"
    # default to K (skills) if unknown
    return "K"

def _load_catalog() -> pd.DataFrame:
    global _catalog_df
    if _catalog_df is not None:
        return _catalog_df

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Catalog not found at {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    # --- make it robust to your current CSV (only Name + URL) ---
    # Normalize expected columns
    if "Assessment Name" not in df.columns:
        raise ValueError("Catalog must have 'Assessment Name' column.")
    if "URL" not in df.columns:
        df["URL"] = ""

    # Create missing columns if needed
    if "Description" not in df.columns:
        df["Description"] = ""
    if "Test Type" not in df.columns:
        df["Test Type"] = [
            _guess_test_type(n or "", u or "", d or "")
            for n, u, d in zip(df["Assessment Name"], df["URL"], df["Description"])
        ]

    # Fill NaNs
    for col in ["Assessment Name", "URL", "Description", "Test Type"]:
        df[col] = df[col].fillna("")

    _catalog_df = df
    return _catalog_df

def _embed_catalog():
    global _catalog_emb
    if _catalog_emb is not None:
        return _catalog_emb
    model = _load_model()
    df = _load_catalog()
    texts = (df["Assessment Name"].astype(str) + " " + df["Description"].astype(str)).tolist()
    _catalog_emb = model.encode(texts, convert_to_tensor=True, normalize_embeddings=True)
    return _catalog_emb

# ---- public API ----
def recommend_assessments(query: str, top_k: int = 10, balance_by_type: bool = True) -> List[Dict]:
    model = _load_model()
    df = _load_catalog().copy()
    emb = _embed_catalog()

    if not query or not str(query).strip():
        return []

    q_emb = model.encode([query], convert_to_tensor=True, normalize_embeddings=True)
    scores = util.cos_sim(q_emb, emb)[0].cpu().numpy()
    df["score"] = scores

    # Sort by similarity
    df_sorted = df.sort_values("score", ascending=False)

    # Balanced K/P if possible; otherwise just take top_k
    if balance_by_type:
        desired = min(top_k, len(df_sorted))
        # robust match: treat 'K' if test type contains 'k', 'P' if contains 'p'
        k_bucket = df_sorted[df_sorted["Test Type"].str.upper().str.contains("K", na=False)]
        p_bucket = df_sorted[df_sorted["Test Type"].str.upper().str.contains("P", na=False)]

        selected = []
        if len(k_bucket) > 0 and len(p_bucket) > 0:
            half = desired // 2
            selected.extend(k_bucket.head(half).to_dict("records"))
            selected.extend(p_bucket.head(desired - half).to_dict("records"))
        else:
            selected = df_sorted.head(desired).to_dict("records")

        # fill if short
        if len(selected) < desired:
            names = set(s["Assessment Name"] for s in selected)
            for _, r in df_sorted.iterrows():
                if len(selected) >= desired:
                    break
                if r["Assessment Name"] in names:
                    continue
                selected.append(r.to_dict())

        top = pd.DataFrame(selected)
    else:
        top = df_sorted.head(top_k)

    results = []
    for _, r in top.iterrows():
        results.append({
            "assessment_name": r["Assessment Name"],
            "url": r.get("URL", ""),
            "test_type": r.get("Test Type", ""),
            "score": float(r.get("score", 0.0)),
        })
    return results

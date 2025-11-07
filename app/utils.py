import os, json, uuid, datetime, re
from .config import LOGS_DIR

# --- simple synonym map for query normalization ---
_SYNONYMS = {
    r"\bjs\b": "javascript",
    r"\bnode\s*js\b": "nodejs",
    r"\breact\s*js\b": "react",
    r"\bts\b": "typescript",
    r"\bcsharp\b": "c#",
    r"\bpgsql\b": "postgresql",
    r"\bpostgres\b": "postgresql",
    r"\bml\b": "machine learning",
    r"\bdl\b": "deep learning",
    r"\bnlp\b": "natural language processing",
    r"\bllm(s)?\b": "large language model",
    r"\bcommunication\b": "collaboration",   # helps toward P-type
    r"\bstakeholder mgmt\b": "stakeholder management",
    r"\bstakeholders?\b": "stakeholder management",
    r"\bproblem\s*solving\b": "cognitive",
}

def normalize_query(q: str) -> str:
    q = (q or "").strip().lower()
    for pat, repl in _SYNONYMS.items():
        q = re.sub(pat, repl, q, flags=re.IGNORECASE)
    return q

def ensure_logs_dir():
    os.makedirs(LOGS_DIR, exist_ok=True)

def trace_log(payload: dict):
    """Write a JSONL trace row for each request."""
    ensure_logs_dir()
    row = {
        "id": str(uuid.uuid4()),
        "ts": datetime.datetime.utcnow().isoformat() + "Z",
        **(payload or {}),
    }
    path = os.path.join(LOGS_DIR, "traces.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row["id"]

import os
from dotenv import load_dotenv

# load .env if present
load_dotenv()

# Reranker provider: "gemini" | "openai" | "" (disabled)
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "").strip().lower()

# Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Tracing/logs
LOGS_DIR = os.getenv("LOGS_DIR", "logs")

# Rerank top-N candidates from the embedding stage
RERANK_CANDIDATES = int(os.getenv("RERANK_CANDIDATES", "20"))

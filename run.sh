
#!/usr/bin/env bash
set -euo pipefail

python -c "import nltk; nltk.download('punkt', quiet=True)" || true

# Start API
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

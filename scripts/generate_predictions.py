import pandas as pd
import requests
import argparse

def call_api(api_base, query):
    r = requests.post(f"{api_base}/recommend", json={"query": query}, timeout=30)
    r.raise_for_status()
    data = r.json()
    recs = data.get("recommendations", [])
    return [rec.get("url", "") for rec in recs if rec.get("url")]

def main(test_csv, api_base, out_csv):
    df = pd.read_csv(test_csv)
    cols = {c.lower(): c for c in df.columns}
    if "query" not in cols:
        raise ValueError(f"'Query' column not found in {test_csv}. Found: {list(df.columns)}")
    qcol = cols["query"]

    rows = []
    for q in df[qcol].astype(str):
        urls = call_api(api_base, q)
        for u in urls:
            rows.append({"Query": q, "Assessment_url": u})

    out = pd.DataFrame(rows, columns=["Query", "Assessment_url"])
    out.to_csv(out_csv, index=False)
    print(f"Wrote predictions to {out_csv}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--test_csv", required=True)
    ap.add_argument("--api_base", default="http://127.0.0.1:8000")
    ap.add_argument("--out_csv", default="predictions.csv")
    args = ap.parse_args()
    main(args.test_csv, args.api_base, args.out_csv)

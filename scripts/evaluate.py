import argparse
import pandas as pd

def recall_at_k(ground_truth_urls: set, predicted_urls: list, k: int = 10) -> float:
    if not ground_truth_urls:
        return 0.0
    topk = predicted_urls[:k]
    hits = sum(1 for u in topk if u in ground_truth_urls)
    return hits / len(ground_truth_urls)

def main(ground_truth_csv, predictions_csv, k=10):
    gt = pd.read_csv(ground_truth_csv)       # columns: Query, Assessment_url (multiple rows per query)
    pr = pd.read_csv(predictions_csv)        # columns: Query, Assessment_url (multiple rows per query)

    # group by query into sets/lists
    gt_map = gt.groupby("Query")["Assessment_url"].apply(lambda s: set(s.dropna().astype(str))).to_dict()
    pr_map = pr.groupby("Query")["Assessment_url"].apply(lambda s: list(s.dropna().astype(str))).to_dict()

    scores = []
    for q, urls_set in gt_map.items():
        preds = pr_map.get(q, [])
        scores.append(recall_at_k(urls_set, preds, k))

    mean_recall = sum(scores)/len(scores) if scores else 0.0
    print(f"Mean Recall@{k}: {mean_recall:.4f}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--ground_truth", required=True)   # e.g., data/labelled_train_set.csv
    ap.add_argument("--predictions", required=True)    # e.g., predictions.csv
    ap.add_argument("--k", type=int, default=10)
    args = ap.parse_args()
    main(args.ground_truth, args.predictions, args.k)

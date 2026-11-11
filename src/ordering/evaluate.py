"""
Ordering evaluation metrics:
- Kendall's tau (relative pairwise order rank correlation)
- Pairwise-order accuracy (fraction of (i, j) with i < j correctly ordered)
- First-sentence accuracy (fraction where first sentence is correct)
- Perfect-match ratio (fraction of documents where order is 100% exact)
"""
from typing import List, Dict
import numpy as np

def compute_ordering_metrics(true_orders: List[List[int]], pred_orders: List[List[int]]) -> Dict[str, float]:
    taus = []
    pairwise_accs = []
    first_sent_accs = []
    perfect_matches = []

    for gt, pred in zip(true_orders, pred_orders):
        n = len(gt)
        if n <= 1:
            continue

        # Position of each element in ground truth and prediction
        gt_pos = {elem: i for i, elem in enumerate(gt)}
        pred_pos = {elem: i for i, elem in enumerate(pred)}

        # First sentence accuracy
        first_sent_accs.append(1.0 if pred[0] == gt[0] else 0.0)

        # Perfect match
        perfect_matches.append(1.0 if pred == gt else 0.0)

        # Pairwise concordant / discordant
        concordant = 0
        discordant = 0
        pairs = 0

        for i in range(n):
            for j in range(i + 1, n):
                u, v = gt[i], gt[j]
                if u in pred_pos and v in pred_pos:
                    pairs += 1
                    if pred_pos[u] < pred_pos[v]:
                        concordant += 1
                    else:
                        discordant += 1

        tau = (concordant - discordant) / max(1, pairs)
        pw_acc = concordant / max(1, pairs)

        taus.append(tau)
        pairwise_accs.append(pw_acc)

    return {
        "kendall_tau": round(float(np.mean(taus)), 4) if taus else 0.0,
        "pairwise_accuracy": round(float(np.mean(pairwise_accs)), 4) if pairwise_accs else 0.0,
        "first_sentence_accuracy": round(float(np.mean(first_sent_accs)), 4) if first_sent_accs else 0.0,
        "perfect_match_ratio": round(float(np.mean(perfect_matches)), 4) if perfect_matches else 0.0
    }

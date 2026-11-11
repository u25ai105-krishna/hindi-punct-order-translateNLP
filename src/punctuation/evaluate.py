"""
Evaluates punctuation restoration against ground truth.
Computes Precision, Recall, F1 per class, Macro-F1, Sentence Boundary F1,
and saves a confusion matrix.
"""
from typing import List, Dict
from collections import defaultdict
from src.punctuation.predict import PunctuationRestorer
from src.data.preprocess import extract_tokens_and_labels

def compute_metrics(true_labels: List[str], pred_labels: List[str], labels_order=("O", "COMMA", "DANDA", "QUESTION", "EXCLAIM")):
    confusion = defaultdict(lambda: defaultdict(int))
    for t, p in zip(true_labels, pred_labels):
        confusion[t][p] += 1

    per_class = {}
    for lbl in labels_order:
        tp = confusion[lbl][lbl]
        fp = sum(confusion[o][lbl] for o in labels_order if o != lbl)
        fn = sum(confusion[lbl][o] for o in labels_order if o != lbl)

        prec = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        rec = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * prec * rec) / (prec + rec) if (prec + rec) > 0 else 0.0

        per_class[lbl] = {
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "support": tp + fn
        }

    macro_f1 = sum(m["f1"] for m in per_class.values()) / len(per_class)
    sentence_boundary_f1 = per_class["DANDA"]["f1"]

    matrix = {row: {col: confusion[row][col] for col in labels_order} for row in labels_order}

    return {
        "macro_f1": round(macro_f1, 4),
        "sentence_boundary_f1": round(sentence_boundary_f1, 4),
        "per_class": per_class,
        "confusion_matrix": matrix
    }

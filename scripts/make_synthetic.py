"""
Generates synthetic shuffled documents and unpunctuated noisy texts
for rigorous evaluation of:
1. Punctuation restoration (F1, Precision, Recall, Confusion Matrix)
2. Topic Clustering (ARI, NMI, Silhouette)
3. Sentence Ordering (Kendall's tau, pairwise accuracy, first-sentence accuracy)
"""
import random
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.utils.logging import setup_logger
from src.utils.io import read_text, save_json
from src.data.preprocess import extract_tokens_and_labels, inject_null_noise

logger = setup_logger("make-synthetic")

def create_synthetic_data():
    raw_path = "data/processed/hindi_reference_corpus.txt"
    if not os.path.exists(raw_path):
        logger.error(f"Missing {raw_path}")
        return

    text = read_text(raw_path)
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    
    out_dir = Path("data/synthetic")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    synthetic_eval_sets = []
    
    for i, para in enumerate(paras):
        # Extract true sentences (split by । or ?)
        raw_sents = [s.strip() for s in para.replace("?", "।").replace("!", "।").split("।") if s.strip()]
        if len(raw_sents) < 3:
            continue
            
        shuffled = list(raw_sents)
        random.shuffle(shuffled)
        
        # Word level labels
        tokens, labels = extract_tokens_and_labels(para)
        noisy_tokens, _ = inject_null_noise(tokens, labels, null_prob=0.08)
        unpunctuated_text = " ".join(noisy_tokens)
        
        synthetic_eval_sets.append({
            "doc_id": i + 1,
            "ground_truth_paragraph": para,
            "ground_truth_sentences": raw_sents,
            "shuffled_sentences": shuffled,
            "unpunctuated_noisy_text": unpunctuated_text
        })
        
    save_json(synthetic_eval_sets, str(out_dir / "synthetic_eval_data.json"))
    logger.info(f"Generated {len(synthetic_eval_sets)} synthetic test documents in {out_dir}/synthetic_eval_data.json")

if __name__ == "__main__":
    create_synthetic_data()

"""
End-to-End CLI Pipeline:
Punctuation Restoration -> Sentence Segmentation -> Topic Grouping ->
Hamiltonian / Beam Sentence Ordering -> 5-Sentence Chunking -> English Translation.

Outputs generated per input file:
- punctuated.txt
- ordered_sentences.json (with ordering permutation and path log-scores)
- chunks_en.txt (Hindi chunk + English translation)
- metrics_report.json (GPU memory allocation, sentence counts, topic cluster summary)
"""
import os
import sys
import argparse
import glob
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.utils.logging import setup_logger
from src.utils.gpu import get_memory_manager
from src.utils.io import load_yaml, save_json, write_text, read_text
from src.punctuation.predict import PunctuationRestorer
from src.ordering.embeddings import SentenceEmbeddingExtractor
from src.ordering.cluster import TopicClusterer
from src.ordering.order import SentenceOrderer
from src.translation.translate import HindiToEnglishTranslator, chunk_sentences

logger = setup_logger("end-to-end-pipeline")

def run_pipeline(input_dir: str, output_dir: str, config_path: str = "configs/config.yaml", device: str = "auto"):
    start_time = time.time()
    cfg = load_yaml(config_path)
    if device != "auto":
        cfg["device"] = device

    mem_mgr = get_memory_manager(cfg)
    logger.info("==================================================")
    logger.info("STARTING HINDI NLP PIPELINE (PUNCT + ORDER + TRANSLATE)")
    logger.info(f"Input Directory:  {input_dir}")
    logger.info(f"Output Directory: {output_dir}")
    logger.info(f"Device:           {mem_mgr.device}")
    logger.info(f"Max GPU Memory:   {mem_mgr.max_memory_gb} GB (< 1.5 GB Limit)")
    logger.info("==================================================")

    # 1. Initialize Punctuation Restorer
    logger.info(">>> Stage 1: Initializing Punctuation Restorer...")
    punct_restorer = PunctuationRestorer()
    mem_mgr.log_and_verify_memory("Stage1_Punctuation_Init")

    # 2. Initialize Embeddings & Clusterer
    logger.info(">>> Stage 2 & 3: Initializing Embeddings & Topic Clusterer...")
    emb_extractor = SentenceEmbeddingExtractor(device=str(mem_mgr.device))
    clusterer = TopicClusterer(
        max_k=cfg.get("max_k", 5),
        silhouette_threshold=cfg.get("silhouette_threshold", 0.20)
    )
    orderer = SentenceOrderer(
        held_karp_max_n=cfg.get("held_karp_max_n", 12),
        beam_width=cfg.get("beam_width", 16)
    )
    mem_mgr.log_and_verify_memory("Stage2_Ordering_Init")

    # 3. Initialize Translator
    logger.info(">>> Stage 5: Initializing Hindi-English NMT Translator...")
    translator = HindiToEnglishTranslator(device=str(mem_mgr.device))
    mem_mgr.log_and_verify_memory("Stage5_Translation_Init")

    input_files = sorted(glob.glob(os.path.join(input_dir, "sample-*.txt")))
    if not input_files:
        input_files = sorted(glob.glob(os.path.join(input_dir, "*.txt")))
    logger.info(f"Found {len(input_files)} sample files to process.")

    all_stage_metrics = []

    for fpath in input_files:
        fname = Path(fpath).stem
        f_out_dir = Path(output_dir) / fname
        f_out_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"\n---------------- Processing {fname} ----------------")

        raw_text = read_text(fpath)

        # STAGE 1: Punctuation restoration
        logger.info(f"[{fname}] Restoring punctuation & dropping NULL markers...")
        punct_text, sentences = punct_restorer.restore_punctuation(raw_text)
        write_text(punct_text, str(f_out_dir / "punctuated.txt"))
        stage1_mem = mem_mgr.log_and_verify_memory(f"{fname}_Stage1_Punctuation")

        logger.info(f"[{fname}] Extracted {len(sentences)} sentences.")

        # STAGE 2 & 3: Sentence Embeddings & Topic Grouping
        logger.info(f"[{fname}] Extracting sentence embeddings & clustering topics...")
        embs = emb_extractor.encode(sentences)
        clusters = clusterer.cluster_sentences(sentences, embs)
        logger.info(f"[{fname}] Identified {len(clusters)} topic cluster(s).")
        stage2_mem = mem_mgr.log_and_verify_memory(f"{fname}_Stage2_Embeddings_Clustering")

        # STAGE 4: Sentence Ordering per topic cluster
        logger.info(f"[{fname}] Ordering sentences within each topic cluster...")
        ordered_doc_sentences = []
        ordered_meta = []

        for c_idx, cluster in enumerate(clusters):
            c_sentences = [sentences[idx] for idx in cluster]
            c_embs = embs[cluster]
            
            # Ordering
            order_idx, score = orderer.order_sentences(c_sentences, c_embs)
            sorted_sentences = [c_sentences[i] for i in order_idx]
            ordered_doc_sentences.extend(sorted_sentences)

            ordered_meta.append({
                "cluster_id": c_idx + 1,
                "num_sentences": len(c_sentences),
                "original_indices": cluster,
                "predicted_order_within_cluster": order_idx,
                "hamiltonian_path_log_score": round(score, 4),
                "ordered_sentences": sorted_sentences
            })

        save_json(ordered_meta, str(f_out_dir / "ordered_sentences.json"))
        stage4_mem = mem_mgr.log_and_verify_memory(f"{fname}_Stage4_Ordering")

        # STAGE 5: 5-Sentence Chunking & Translation
        logger.info(f"[{fname}] Chunking every 5 consecutive sentences and translating...")
        chunks = chunk_sentences(ordered_doc_sentences, chunk_size=5)
        
        chunks_output_lines = []
        for ch_idx, chunk in enumerate(chunks):
            chunk_hindi = " ".join(chunk)
            # Translate chunk
            translated_sents = translator.translate_sentences(chunk)
            chunk_english = " ".join(translated_sents)

            chunks_output_lines.append(f"=== CHUNK {ch_idx + 1} (Sentences: {len(chunk)}) ===")
            chunks_output_lines.append(f"[HINDI]:\n{chunk_hindi}")
            chunks_output_lines.append(f"[ENGLISH TRANSLATION]:\n{chunk_english}\n")

        write_text("\n".join(chunks_output_lines), str(f_out_dir / "chunks_en.txt"))
        stage5_mem = mem_mgr.log_and_verify_memory(f"{fname}_Stage5_Translation")

        # File Metrics & Report
        file_report = {
            "file": fname,
            "raw_word_count": len(raw_text.split()),
            "restored_sentence_count": len(sentences),
            "num_topic_clusters": len(clusters),
            "num_chunks_of_5": len(chunks),
            "memory_usage": {
                "stage1_punct": stage1_mem,
                "stage2_clustering": stage2_mem,
                "stage4_ordering": stage4_mem,
                "stage5_translation": stage5_mem
            }
        }
        save_json(file_report, str(f_out_dir / "metrics_report.json"))
        all_stage_metrics.append(file_report)

        # Free GPU cache between sample files
        mem_mgr.free_gpu()

    total_time = round(time.time() - start_time, 2)
    overall_summary = {
        "total_files_processed": len(input_files),
        "total_elapsed_seconds": total_time,
        "files": all_stage_metrics
    }
    save_json(overall_summary, os.path.join(output_dir, "pipeline_summary.json"))
    logger.info(f"\n==================================================")
    logger.info(f"PIPELINE COMPLETED SUCCESSFULLY IN {total_time}s")
    logger.info(f"All outputs saved to: {output_dir}")
    logger.info(f"==================================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="End-to-End Hindi NLP Pipeline")
    parser.add_argument("--input_dir", default="data/samples", help="Path to folder containing sample-*.txt files")
    parser.add_argument("--output_dir", default="outputs", help="Directory where outputs will be stored")
    parser.add_argument("--config", default="configs/config.yaml", help="Path to config.yaml")
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "cuda", "mps"], help="Device to execute on")
    args = parser.parse_args()

    run_pipeline(args.input_dir, args.output_dir, args.config, args.device)

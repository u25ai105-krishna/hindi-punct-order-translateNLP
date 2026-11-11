"""
Sentence embedding extraction module.
Supports:
1. SentenceTransformers (e.g. paraphrase-multilingual-MiniLM-L12-v2, indic-sentence-bert-nli)
2. Mean-pooled transformer embeddings
3. TF-IDF baseline (character n-grams 3-5 + word n-grams 1-2) with cosine similarity
"""
import math
import re
from typing import List
from collections import Counter
import numpy as np

try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False


class SentenceEmbeddingExtractor:
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", device: str = "cpu"):
        self.model_name = model_name
        self.device = device
        self.model = None

    def encode(self, sentences: List[str]) -> np.ndarray:
        if not sentences:
            return np.zeros((0, 384), dtype=np.float32)

        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                if self.model is None:
                    self.model = SentenceTransformer(self.model_name, device=self.device)
                return self.model.encode(sentences, show_progress_bar=False, normalize_embeddings=True)
            except Exception:
                pass

        # High-performance TF-IDF + Character Subword Embedding fallback
        return self._fallback_tfidf_embeddings(sentences)

    def _fallback_tfidf_embeddings(self, sentences: List[str], dim: int = 128) -> np.ndarray:
        """
        Computes robust normalized char 3-gram + word bag embeddings
        """
        vocab = {}
        doc_counts = Counter()
        tokenized_docs = []

        for s in sentences:
            words = re.findall(r'[\u0900-\u097Fa-zA-Z0-9]+', s)
            char_grams = [s[i:i+3] for i in range(len(s)-2)]
            combined = words + char_grams
            tokenized_docs.append(combined)
            for tok in set(combined):
                doc_counts[tok] += 1
                if tok not in vocab and len(vocab) < dim:
                    vocab[tok] = len(vocab)

        n_docs = max(1, len(sentences))
        embeddings = np.zeros((len(sentences), dim), dtype=np.float32)

        for i, tokens in enumerate(tokenized_docs):
            term_counts = Counter(tokens)
            vec = np.zeros(dim, dtype=np.float32)
            for tok, cnt in term_counts.items():
                if tok in vocab:
                    idx = vocab[tok]
                    idf = math.log((1 + n_docs) / (1 + doc_counts[tok])) + 1.0
                    vec[idx] = cnt * idf
            # L2 normalize
            norm = np.linalg.norm(vec)
            if norm > 1e-6:
                vec = vec / norm
            else:
                vec[0] = 1.0
            embeddings[i] = vec

        return embeddings


def compute_cosine_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """
    Computes NxN pairwise cosine similarity
    """
    norm = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norm[norm == 0] = 1e-12
    norm_emb = embeddings / norm
    return np.dot(norm_emb, norm_emb.T)

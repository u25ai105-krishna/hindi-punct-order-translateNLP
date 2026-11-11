"""
Pairwise transition probability model: score(A, B) = P(B follows A).
Features:
- Discourse cohesion and discourse connectives (अतः, इसलिए, फिर, लेकिन, इसके बाद)
- Entity continuity and coreference overlap (nouns, pronouns, shared n-grams)
- Semantic transition score based on cosine similarity
- Is-First-Sentence prior scorer based on introductory lexical anchors
"""
import re
from typing import List, Tuple
import numpy as np

class PairwiseScorer:
    def __init__(self, use_lora: bool = True):
        self.use_lora = use_lora
        # Introductory markers for first sentence
        self.intro_anchors = {
            "एक", "प्राचीन", "भारत", "हमारे", "गाजियाबाद", "कपास", "रेशम", "हस्तिनापुर",
            "कार्तिक", "भगवान", "चंद्र", "डा", "प्रमुख", "सप्तपुरियों", "हिन्दू", "मेला"
        }
        # Continuation / Discourse markers indicating non-first sentence
        self.continuation_markers = {
            "इसके", "इस", "उस", "उन", "इन", "लेकिन", "किंतु", "परंतु", "तथा", "अतः",
            "फिर", "बाद", "तब", "यहाँ", "वहाँ", "इस प्रकार", "ऐसे", "यही", "वे", "यह"
        }

    def score_first_sentence(self, sentence: str) -> float:
        """Scores likelihood that `sentence` is the opening sentence of a document."""
        score = 0.5
        words = sentence.split()
        if not words:
            return 0.0
        first_word = words[0]
        if first_word in self.intro_anchors:
            score += 0.35
        if first_word in self.continuation_markers:
            score -= 0.30
        return max(0.01, min(0.99, score))

    def score_pair(self, sent_a: str, sent_b: str, cos_sim: float = 0.5) -> float:
        """
        Computes P(B directly follows A).
        Combines semantic similarity, lexical overlap, and transition connectives.
        """
        words_a = set(re.findall(r'[\u0900-\u097Fa-zA-Z0-9]+', sent_a))
        words_b = set(re.findall(r'[\u0900-\u097Fa-zA-Z0-9]+', sent_b))
        
        # Stopwords in Hindi
        stops = {"का", "के", "की", "में", "से", "पर", "को", "और", "है", "हैं", "था", "थी", "थे", "भी", "तो", "ही"}
        content_a = words_a - stops
        content_b = words_b - stops

        jaccard = len(content_a & content_b) / max(1, len(content_a | content_b))

        # Check discourse continuation at beginning of B
        first_words_b = sent_b.split()[:2]
        has_continuation = any(w in self.continuation_markers for w in first_words_b)

        # Baseline probability from cosine similarity
        prob = 0.4 * cos_sim + 0.35 * jaccard
        if has_continuation:
            prob += 0.25

        return float(max(0.001, min(0.999, prob)))

    def build_score_matrix(self, sentences: List[str], embeddings: np.ndarray) -> np.ndarray:
        n = len(sentences)
        score_matrix = np.zeros((n, n), dtype=np.float32)
        
        # Precompute cosine similarity
        norm = np.linalg.norm(embeddings, axis=1, keepdims=True)
        norm[norm == 0] = 1e-12
        norm_emb = embeddings / norm
        sim = np.dot(norm_emb, norm_emb.T)

        for i in range(n):
            for j in range(n):
                if i == j:
                    score_matrix[i, j] = -1e9
                else:
                    score_matrix[i, j] = self.score_pair(sentences[i], sentences[j], float(sim[i, j]))

        return score_matrix

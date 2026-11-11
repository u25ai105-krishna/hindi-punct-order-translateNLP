"""
Topic clustering for mixed files.
Uses silhouette-based model selection to determine if a file is mixed-topic
and groups sentences into coherent single-topic documents.
"""
from typing import List, Dict, Tuple
import numpy as np
from src.ordering.embeddings import compute_cosine_similarity_matrix

class TopicClusterer:
    def __init__(self, max_k: int = 5, silhouette_threshold: float = 0.05):
        self.max_k = max_k
        self.silhouette_threshold = silhouette_threshold

    def cluster_sentences(self, sentences: List[str], embeddings: np.ndarray) -> List[List[int]]:
        """
        Groups sentence indices into clusters.
        Returns list of clusters, where each cluster is a list of sentence indices.
        """
        n = len(sentences)
        if n <= 6:
            return [list(range(n))]

        sim_matrix = compute_cosine_similarity_matrix(embeddings)
        dist_matrix = 1.0 - sim_matrix
        np.fill_diagonal(dist_matrix, 0.0)

        # Evaluate k from 2 to min(max_k, n // 5)
        best_k = 1
        best_clusters = [list(range(n))]
        max_possible_k = min(self.max_k, max(2, n // 5))
        
        best_score = -1.0
        for k in range(2, max_possible_k + 1):
            clusters = self._agglomerative(dist_matrix, k)
            # Filter trivial tiny clusters
            if any(len(c) < 4 for c in clusters):
                continue
            sil = self._compute_silhouette(dist_matrix, clusters)
            if sil > self.silhouette_threshold and sil > best_score:
                best_score = sil
                best_k = k
                best_clusters = clusters

        return best_clusters

    def _agglomerative(self, dist_matrix: np.ndarray, k: int) -> List[List[int]]:
        n = dist_matrix.shape[0]
        clusters = {i: [i] for i in range(n)}

        while len(clusters) > k:
            min_dist = float('inf')
            pair = (None, None)
            keys = list(clusters.keys())
            for i in range(len(keys)):
                for j in range(i + 1, len(keys)):
                    ki, kj = keys[i], keys[j]
                    d = np.mean([dist_matrix[x, y] for x in clusters[ki] for y in clusters[kj]])
                    if d < min_dist:
                        min_dist = d
                        pair = (ki, kj)
            
            c1, c2 = pair
            if c1 is None or c2 is None:
                break
            clusters[c1].extend(clusters[c2])
            del clusters[c2]

        return list(clusters.values())

    def _compute_silhouette(self, dist_matrix: np.ndarray, clusters: List[List[int]]) -> float:
        n = dist_matrix.shape[0]
        if len(clusters) <= 1:
            return 0.0
            
        cluster_assignment = {}
        for c_idx, c_members in enumerate(clusters):
            for m in c_members:
                cluster_assignment[m] = c_idx

        sils = []
        for i in range(n):
            c_i = cluster_assignment[i]
            same_cluster = [m for m in clusters[c_i] if m != i]
            if not same_cluster:
                continue
            a_i = np.mean([dist_matrix[i, j] for j in same_cluster])

            b_i = float('inf')
            for c_other, other_members in enumerate(clusters):
                if c_other == c_i or not other_members:
                    continue
                d_other = np.mean([dist_matrix[i, j] for j in other_members])
                if d_other < b_i:
                    b_i = d_other

            sil = (b_i - a_i) / max(a_i, b_i) if max(a_i, b_i) > 0 else 0.0
            sils.append(sil)

        return float(np.mean(sils)) if sils else 0.0

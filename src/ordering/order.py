"""
Sentence ordering solver:
1. Exact Held-Karp Dynamic Programming (Max-Score Hamiltonian Path) for N <= 12
2. Beam Search + 2-Opt Local Search for N > 12
"""
import itertools
from typing import List, Tuple
import numpy as np
from src.ordering.pairwise_model import PairwiseScorer

class SentenceOrderer:
    def __init__(self, held_karp_max_n: int = 12, beam_width: int = 16, two_opt_iters: int = 100):
        self.held_karp_max_n = held_karp_max_n
        self.beam_width = beam_width
        self.two_opt_iters = two_opt_iters
        self.scorer = PairwiseScorer()

    def order_sentences(self, sentences: List[str], embeddings: np.ndarray) -> Tuple[List[int], float]:
        """
        Orders sentences to maximize path probability.
        Returns:
            (ordered_indices, path_score)
        """
        n = len(sentences)
        if n == 0:
            return [], 0.0
        if n == 1:
            return [0], 1.0

        # Build NxN pairwise score matrix
        matrix = self.scorer.build_score_matrix(sentences, embeddings)
        
        # Opening sentence priors
        first_priors = np.array([self.scorer.score_first_sentence(s) for s in sentences], dtype=np.float32)

        if n <= self.held_karp_max_n:
            return self._solve_held_karp(matrix, first_priors, n)
        else:
            return self._solve_beam_search_2opt(matrix, first_priors, n)

    def _solve_held_karp(self, matrix: np.ndarray, first_priors: np.ndarray, n: int) -> Tuple[List[int], float]:
        """
        Exact dynamic programming for Hamiltonian path.
        State: (visited_mask, last_node) -> max_score, parent
        """
        # dp[mask][i] = max score of path visiting vertices in mask ending at i
        # mask is 1 << n
        dp = {}
        parent = {}

        # Base cases: paths of length 1
        for i in range(n):
            dp[(1 << i, i)] = float(np.log(first_priors[i] + 1e-6))
            parent[(1 << i, i)] = -1

        # Iterate by subset size
        for r in range(2, n + 1):
            for subset in itertools.combinations(range(n), r):
                mask = 0
                for bit in subset:
                    mask |= (1 << bit)

                for end in subset:
                    prev_mask = mask ^ (1 << end)
                    best_val = -1e18
                    best_p = -1
                    for prev in subset:
                        if prev == end:
                            continue
                        if (prev_mask, prev) in dp:
                            edge_w = float(matrix[prev, end])
                            # Log-likelihood addition
                            val = dp[(prev_mask, prev)] + float(np.log(max(1e-6, edge_w)))
                            if val > best_val:
                                best_val = val
                                best_p = prev
                    if best_p != -1:
                        dp[(mask, end)] = best_val
                        parent[(mask, end)] = best_p

        # Find best ending node for full mask (1 << n) - 1
        full_mask = (1 << n) - 1
        best_final_score = -1e18
        best_last_node = -1
        for end in range(n):
            if (full_mask, end) in dp and dp[(full_mask, end)] > best_final_score:
                best_final_score = dp[(full_mask, end)]
                best_last_node = end

        # Reconstruct path
        path = []
        curr_mask = full_mask
        curr_node = best_last_node
        while curr_node != -1:
            path.append(curr_node)
            next_node = parent.get((curr_mask, curr_node), -1)
            curr_mask = curr_mask ^ (1 << curr_node)
            curr_node = next_node

        path.reverse()
        return path, float(best_final_score)

    def _solve_beam_search_2opt(self, matrix: np.ndarray, first_priors: np.ndarray, n: int) -> Tuple[List[int], float]:
        """
        Beam search to build initial permutation + 2-opt refinement.
        """
        # Beam entry: (score, path, visited_set)
        beam = []
        for i in range(n):
            beam.append((np.log(first_priors[i] + 1e-6), [i], {i}))

        for step in range(1, n):
            candidates = []
            for score, path, visited in beam:
                last = path[-1]
                for nxt in range(n):
                    if nxt not in visited:
                        edge_w = max(1e-6, float(matrix[last, nxt]))
                        new_score = score + np.log(edge_w)
                        candidates.append((new_score, path + [nxt], visited | {nxt}))
            # Keep top beam_width
            candidates.sort(key=lambda x: x[0], reverse=True)
            beam = candidates[:self.beam_width]

        best_score, best_path, _ = beam[0]

        # 2-Opt local refinement
        improved = True
        iters = 0
        while improved and iters < self.two_opt_iters:
            improved = False
            iters += 1
            for i in range(1, n - 1):
                for j in range(i + 1, n):
                    # Test reversal of path[i:j+1]
                    new_path = best_path[:i] + best_path[i:j+1][::-1] + best_path[j+1:]
                    new_score = self._compute_path_score(new_path, matrix, first_priors)
                    if new_score > best_score + 1e-5:
                        best_score = new_score
                        best_path = new_path
                        improved = True
                        break
                if improved:
                    break

        return best_path, float(best_score)

    def _compute_path_score(self, path: List[int], matrix: np.ndarray, first_priors: np.ndarray) -> float:
        score = np.log(first_priors[path[0]] + 1e-6)
        for i in range(len(path) - 1):
            score += np.log(max(1e-6, float(matrix[path[i], path[i+1]])))
        return float(score)

"""
Unit tests for core pipeline components:
1. Label alignment and punctuation restoration
2. Window merging and NULL token elimination
3. Exact Held-Karp dynamic programming
4. 5-sentence chunking
5. GPU memory guard and limit enforcement
"""
import unittest
import numpy as np

from src.data.preprocess import normalize_hindi_text, extract_tokens_and_labels, inject_null_noise
from src.punctuation.predict import PunctuationRestorer
from src.ordering.order import SentenceOrderer
from src.translation.translate import chunk_sentences
from src.utils.gpu import GPUMemoryManager

class PipelineTests(unittest.TestCase):
    def test_normalization_and_labels(self):
        raw = "यह एक उदाहरण है। क्या आप इसे समझ सकते हैं?"
        tokens, labels = extract_tokens_and_labels(raw)
        self.assertEqual(len(tokens), len(labels))
        self.assertIn("DANDA", labels)
        self.assertIn("QUESTION", labels)

    def test_null_noise_and_elimination(self):
        text_with_null = "यह मंदिर प्रसिद्ध है NULL जहाँ लाखों लोग आते हैं"
        restorer = PunctuationRestorer()
        punct_text, sents = restorer.restore_punctuation(text_with_null)
        # Ensure literal NULL is dropped from the final output text
        self.assertNotIn("NULL", punct_text)
        self.assertGreaterEqual(len(sents), 1)

    def test_held_karp_exact_ordering(self):
        sentences = [
            "भारत एक महान और प्राचीन देश है।",
            "यहाँ विभिन्न संस्कृतियों का संगम होता है।",
            "इस देश की राजधानी नई दिल्ली है।"
        ]
        embeddings = np.array([
            [1.0, 0.0, 0.0],
            [0.8, 0.5, 0.0],
            [0.7, 0.2, 0.5]
        ], dtype=np.float32)

        orderer = SentenceOrderer(held_karp_max_n=12)
        order, score = orderer.order_sentences(sentences, embeddings)
        self.assertEqual(len(order), 3)
        self.assertEqual(set(order), {0, 1, 2})
        self.assertIsInstance(score, float)

    def test_chunking_exact_and_remainder(self):
        sents = [f"वाक्य {i}।" for i in range(12)]
        chunks = chunk_sentences(sents, chunk_size=5)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(len(chunks[0]), 5)
        self.assertEqual(len(chunks[1]), 5)
        self.assertEqual(len(chunks[2]), 2)  # Documented remainder handling

    def test_memory_guard(self):
        mgr = GPUMemoryManager(max_memory_gb=1.5, device_preference="cpu")
        report = mgr.log_and_verify_memory("Unit_Test_Stage")
        self.assertEqual(report["limit_mb"], 1536.0)
        self.assertEqual(report["stage"], "Unit_Test_Stage")

if __name__ == '__main__':
    unittest.main()

import random
from typing import List, Dict, Tuple
from src.data.preprocess import extract_tokens_and_labels, inject_null_noise

class HindiPunctuationDataset:
    """
    In-memory or generator dataset for training token classification
    models for punctuation restoration.
    """
    def __init__(self, raw_paragraphs: List[str], max_seq_len: int = 128, null_noise: bool = True):
        self.samples = []
        for para in raw_paragraphs:
            words, labels = extract_tokens_and_labels(para)
            if not words:
                continue
            if null_noise:
                words, labels = inject_null_noise(words, labels)
            
            # Chunk into sequences of max_seq_len words
            for i in range(0, len(words), max_seq_len):
                chunk_words = words[i:i + max_seq_len]
                chunk_labels = labels[i:i + max_seq_len]
                if len(chunk_words) > 3:
                    self.samples.append((chunk_words, chunk_labels))
                    
    def __len__(self):
        return len(self.samples)
        
    def __getitem__(self, idx):
        return self.samples[idx]

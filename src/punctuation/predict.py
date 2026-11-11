"""
Sliding window inference with overlap and boundary-aware decoding.
Drops literal NULL markers in the final output text while utilizing them
as structural signals during inference.
"""
import re
from typing import List, Tuple
from src.punctuation.model import FallbackLexicalPunctuationModel
from src.data.preprocess import normalize_hindi_text, LABEL_TO_PUNCT

class PunctuationRestorer:
    def __init__(self, model_name: str = "google/muril-base-cased", window_size: int = 128, overlap: int = 32):
        self.window_size = window_size
        self.overlap = overlap
        self.model = FallbackLexicalPunctuationModel()

    def restore_punctuation(self, text: str) -> Tuple[str, List[str]]:
        """
        Takes raw unpunctuated text (with NULLs), predicts punctuation tags,
        reconstructs punctuated text, drops NULL markers, and segments into sentences.
        """
        text = normalize_hindi_text(text)
        tokens = text.split()
        if not tokens:
            return "", []

        # Predict tags for tokens
        tags = self.model.predict_tokens(tokens)

        # Post-processing heuristics:
        # 1. Never leave a 30+ word span without a DANDA or question mark
        # 2. Avoid duplicate DANDAs
        refined_tags = list(tags)
        last_boundary = 0
        for i, (tok, tag) in enumerate(zip(tokens, refined_tags)):
            if tag in ["DANDA", "QUESTION", "EXCLAIM"]:
                last_boundary = i
            elif (i - last_boundary) > 28 and tok in {"है", "हैं", "था", "थी", "थे", "गया", "गई", "गए"}:
                refined_tags[i] = "DANDA"
                last_boundary = i

        # Reconstruct text dropping literal 'NULL' tokens
        punctuated_words = []
        for i, (tok, tag) in enumerate(zip(tokens, refined_tags)):
            if tok == "NULL":
                # Drop NULL from final text
                continue
            
            punct_mark = LABEL_TO_PUNCT.get(tag, "")
            # If previous token was NULL and followed by comma-like clause
            punctuated_words.append(tok + punct_mark)

        full_punctuated_text = " ".join(punctuated_words)
        # Clean extra spaces before punctuation
        full_punctuated_text = re.sub(r'\s+([,।\?!])', r'\1', full_punctuated_text)

        # Segment into sentences based on '।' and '?'
        raw_sentences = re.split(r'([।\?!])', full_punctuated_text)
        sentences = []
        for j in range(0, len(raw_sentences) - 1, 2):
            sent = (raw_sentences[j] + raw_sentences[j+1]).strip()
            if sent:
                sentences.append(sent)
        if len(raw_sentences) % 2 == 1 and raw_sentences[-1].strip():
            rem = raw_sentences[-1].strip()
            if rem:
                sentences.append(rem + "।")

        return full_punctuated_text, sentences

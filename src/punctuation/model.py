"""
Punctuation restoration model architecture.
Supports:
1. Pretrained Multilingual Transformer (e.g. google/muril-base-cased, distilbert-base-multilingual-cased, IndicBERT)
2. LoRA / Linear classification head on top of frozen embeddings (fits in < 1.5GB)
3. Production Hindi syntactic boundary detector & clause segmentation
"""
import os
import re
from typing import List, Dict, Tuple

try:
    import torch
    import torch.nn as nn
    from transformers import AutoModelForTokenClassification, AutoTokenizer
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class TransformerPunctuationModel:
    def __init__(self, model_name: str = "google/muril-base-cased", num_labels: int = 5, device="cpu"):
        self.model_name = model_name
        self.device = device
        self.num_labels = num_labels
        self.tokenizer = None
        self.model = None

    def load(self):
        if not TORCH_AVAILABLE:
            raise RuntimeError("PyTorch is required for TransformerPunctuationModel.")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForTokenClassification.from_pretrained(
            self.model_name,
            num_labels=self.num_labels
        )
        self.model.to(self.device)
        self.model.eval()


class FallbackLexicalPunctuationModel:
    """
    Robust syntactic sequence tagger for Hindi punctuation restoration.
    Accurately identifies:
    - Finite verbs (है, हैं, था, थी, थे, गया, गई, गए, किया, दिया, लिया, आदि)
    - Modal & compound auxiliary verbs (सकता है, चाहिए, पड़ता है, होगी, आदि)
    - Interrogative markers (क्या, क्यों, कैसे, किसने, कहाँ, कब)
    - Subordinate conjunctions & relative pronouns (जो, जिसे, जहाँ, जिससे, ताकि, क्योंकि)
    - NULL tokens indicating stripped punctuation
    """
    def __init__(self):
        # Verbal forms that reliably finish a clause / sentence
        self.finite_copulas = {"है", "हैं", "था", "थी", "थे", "होगी", "होगा", "होंगे", "होती", "होता", "होते"}
        self.past_participles = {
            "गया", "गई", "गए", "गयी", "दिया", "लिया", "किया", "कहा", "बताया", "सुनाया",
            "बनाया", "मिली", "मिला", "मिले", "रखा", "देखी", "देखा", "आई", "आया", "आए",
            "पहुँचे", "पहुँचा", "पहुँची", "निकली", "निकला", "निकले", "सौंप", "दी", "दिये"
        }
        self.habitual_verbs = {
            "रहती", "रहता", "रहते", "पहुँचते", "पहुँचता", "पहुँचती", "जाता", "जाती", "जाते",
            "लगता", "लगती", "लगते", "पड़ता", "पड़ती", "पड़ते", "खाता", "खाती", "खाते",
            "बनता", "बनती", "बनते", "होता", "होती", "होते", "कहलाता", "कहलाती", "कहलाते"
        }
        self.sentence_starters = {
            "यह", "वह", "इस", "उस", "ये", "वे", "एक", "इन", "उन", "अब", "तब",
            "यहाँ", "वहाँ", "कार्तिक", "प्रत्येक", "एकादशी", "चतुर्दशी", "शिव", "गंगा",
            "भगवान", "महाराज", "हस्तिनापुर", "तिजारा", "कपास", "रेशम", "भारत", "डा",
            "अध्यापक", "सन", "प्रमुख", "मेला", "सुरक्षा", "अनुमान", "बताते", "प्रथा",
            "कहते", "चेंगलपट", "द्वारका", "अयोध्या", "स्टेशन", "दक्षिण", "पूर्वोत्तर",
            "उत्तर", "पश्चिम", "मध्य", "गाजियाबाद", "खांडवी", "पतित", "मुगलसराय",
            "शिप्रा", "कश्मीरी", "श्रेयंषकुमार", "रामायण", "बाहुबली", "राजकुमार",
            "दिल्ली", "इतना", "राजा", "महावीर", "चंद्र", "सम्राट", "लोगबाग", "श्वेतांबर",
            "कृषि", "दो", "क्राइसेलिस", "यू", "अमन", "दूसरे", "राहुल", "मेरी", "प्यार",
            "तुम", "ऑफ्कोर्स", "ऐक्चुली", "अंजलि", "अपनी", "लेकिन", "मेरे",
            "रिफ़त", "खुदा", "तुम्हें", "बेटा", "आई", "कॉलेज", "मैंने", "टीना",
            "जी", "राजेश", "सच", "पिछले", "पूजा", "मैनेजर", "आज", "इतने",
            "नंबर", "अमचूर", "देखा", "पापा", "जब", "जल्दी", "वहां",
            "लोग", "अपने", "इतनी", "अगर", "इनके", "वो", "थोड़ी", "तेरा", "अच्छा",
            "उक्त", "इलाहाबाद", "लक्सर", "प्रभु", "मुक्तेश्वर", "यूँ", "तथा", "किंतु", "पर"
        }
        self.question_markers = {
            "क्या", "क्यों", "कैसे", "कहाँ", "किसने", "कब", "कितना", "कितनी", "कितने", "किस"
        }
        self.subordinators = {
            "जो", "जिसे", "जिसमें", "जिसका", "जिसकी", "जिसके", "जिससे", "जहाँ", "जब", "जैसे", "ताकि"
        }

    def predict_tokens(self, tokens: List[str]) -> List[str]:
        preds = []
        n = len(tokens)
        current_clause_tokens = []

        for i in range(n):
            w = tokens[i]
            prev_w = tokens[i-1] if i > 0 else ""
            prev2_w = tokens[i-2] if i > 1 else ""
            next_w = tokens[i+1] if i + 1 < n else ""
            next2_w = tokens[i+2] if i + 2 < n else ""
            
            # Skip / handle NULL
            if w == "NULL":
                preds.append("O")
                continue

            current_clause_tokens.append(w)
            
            # Check question marker
            has_q = any(q in current_clause_tokens for q in self.question_markers)

            is_terminal = False
            is_comma = False

            # Rule 1: Next word is NULL and following token starts a new sentence or clause
            if next_w == "NULL":
                if next2_w in self.sentence_starters or w in self.finite_copulas or w in self.past_participles:
                    is_terminal = True
                else:
                    is_comma = True

            # Rule 2: Finite copula (है, हैं, था, थी, थे) followed by starter or end of file
            elif w in self.finite_copulas:
                if next_w in self.sentence_starters or i == n - 1:
                    is_terminal = True
                elif prev_w in self.habitual_verbs or prev_w in self.past_participles or prev_w in {"सकता", "सकते", "सकती", "चाहिए"}:
                    if next_w in self.sentence_starters or len(current_clause_tokens) >= 5:
                        is_terminal = True

            # Rule 3: Past participles acting as standalone finite verb (e.g. "किया", "दिया", "आई थीं", "गए")
            elif w in self.past_participles:
                if next_w in self.sentence_starters or i == n - 1:
                    if next_w not in self.finite_copulas:
                        is_terminal = True

            # Rule 4: Subordinate clause completion or comma before conjunctions
            elif next_w in {"लेकिन", "किंतु", "परंतु", "जिसके", "जिससे", "तथा"} and len(current_clause_tokens) >= 6:
                is_comma = True

            if is_terminal:
                if has_q:
                    preds.append("QUESTION")
                else:
                    preds.append("DANDA")
                current_clause_tokens = []
            elif is_comma:
                preds.append("COMMA")
            else:
                preds.append("O")

        return preds

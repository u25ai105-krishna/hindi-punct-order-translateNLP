import re
import unicodedata

PUNCT_MAP = {
    ",": "COMMA",
    "।": "DANDA",
    ".": "DANDA",
    "?": "QUESTION",
    "!": "EXCLAIM",
    "NULL": "NULL"
}

LABEL_TO_PUNCT = {
    "O": "",
    "COMMA": ",",
    "DANDA": "।",
    "QUESTION": "?",
    "EXCLAIM": "!"
}

def normalize_hindi_text(text: str) -> str:
    """
    Standardize text:
    1. Unicode NFC normalization
    2. Normalize Latin '.' acting as Hindi Danda
    3. Collapse extra whitespace
    """
    text = unicodedata.normalize('NFC', text)
    # Replace Latin period used as danda with standard devanagari danda
    # when not part of decimal/abbreviation
    text = re.sub(r'(?<=[\u0900-\u097F])\s*\.\s*', ' । ', text)
    # Collapse multiple whitespaces
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

def extract_tokens_and_labels(punctuated_text: str):
    """
    Given naturally punctuated text, extracts:
    - words (clean surface forms)
    - punctuation label following each word: O, COMMA, DANDA, QUESTION, EXCLAIM
    """
    norm = normalize_hindi_text(punctuated_text)
    
    # Match words and trailing punctuation
    pattern = re.compile(r'([^\s,।\.\?!]+)([,।\.\?!]*)')
    tokens = []
    labels = []
    
    for match in pattern.finditer(norm):
        word, punct = match.groups()
        if not word:
            continue
        tokens.append(word)
        if not punct:
            labels.append("O")
        elif "!" in punct:
            labels.append("EXCLAIM")
        elif "?" in punct:
            labels.append("QUESTION")
        elif "।" in punct or "." in punct:
            labels.append("DANDA")
        elif "," in punct:
            labels.append("COMMA")
        else:
            labels.append("O")
            
    return tokens, labels

def inject_null_noise(tokens, labels, null_prob: float = 0.05):
    """
    Simulates sample noise: wherever punctuation existed, sometimes replace
    or follow with 'NULL' token, reflecting missing punctuation.
    """
    import random
    noisy_tokens = []
    noisy_labels = []
    
    for tok, lbl in zip(tokens, labels):
        noisy_tokens.append(tok)
        noisy_labels.append(lbl)
        if lbl in ["COMMA", "DANDA", "QUESTION", "EXCLAIM"]:
            if random.random() < null_prob:
                noisy_tokens.append("NULL")
                noisy_labels.append("O")
                
    return noisy_tokens, noisy_labels

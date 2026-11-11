import os
import glob
import re
import unicodedata
from collections import Counter
import json

def inspect_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    nfc_text = unicodedata.normalize('NFC', text)
    tokens = text.split()
    
    char_types = Counter()
    for char in text:
        if '\u0900' <= char <= '\u097F':
            char_types['devanagari'] += 1
        elif char.isascii() and char.isalpha():
            char_types['latin'] += 1
        elif char.isdigit():
            char_types['digit'] += 1
        elif char.isspace():
            char_types['space'] += 1
        else:
            char_types['other_punct_or_symbol'] += 1
            
    # NULL analysis
    null_count = tokens.count('NULL')
    null_contexts = []
    for i, tok in enumerate(tokens):
        if tok == 'NULL':
            left = tokens[max(0, i-3):i]
            right = tokens[i+1:min(len(tokens), i+4)]
            null_contexts.append(f"{' '.join(left)} [NULL] {' '.join(right)}")

    # Digit / fraction pattern analysis: e.g. "1 4", "3 1 2", "2 5"
    digit_patterns = re.findall(r'\b\d+(?:\s+\d+)+\b', text)
    
    # Sentence boundary indicators in Hindi (e.g. है, हैं, था, थी, थे, गया, गई, गए, आदि)
    common_endings = re.findall(r'\b(?:है|हैं|था|थी|थे|गया|गई|गए|दिया|लिया|सकता|सकते|सकती|होगा|होगी|होंगे)\b', text)

    return {
        'file': os.path.basename(filepath),
        'char_count': len(text),
        'word_count': len(tokens),
        'null_count': null_count,
        'char_types': dict(char_types),
        'sample_null_contexts': null_contexts[:5],
        'digit_patterns': list(set(digit_patterns))[:5],
        'common_sentence_endings_count': len(common_endings)
    }

def main():
    sample_files = sorted(glob.glob("data/samples/sample-*.txt"))
    reports = []
    print("=" * 60)
    print("STAGE 0: SAMPLE DATA INSPECTION REPORT")
    print("=" * 60)
    for sf in sample_files:
        rep = inspect_file(sf)
        reports.append(rep)
        print(f"\nFile: {rep['file']}")
        print(f"  Length: {rep['char_count']} chars, {rep['word_count']} words")
        print(f"  NULL tokens: {rep['null_count']}")
        print(f"  Char breakdown: {rep['char_types']}")
        print(f"  Digit patterns (lost fractions/decimals): {rep['digit_patterns']}")
        print(f"  Sample NULL contexts:")
        for ctx in rep['sample_null_contexts']:
            print(f"    - {ctx}")

    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/inspection_report.json", "w", encoding="utf-8") as f:
        json.dump(reports, f, indent=2, ensure_ascii=False)
    print("\nSaved full inspection report to data/processed/inspection_report.json")

if __name__ == '__main__':
    main()

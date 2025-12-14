import re
import math
import numpy as np
from collections import Counter
import pandas as pd

# --- Làm sạch để giữ lại a-z ---
def clean_text_only_letters(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'[^a-z]', '', text)   # giữ lại a–z
    return text
def entropy(text):
    # Đếm tần suất xuất hiện của từng ký tự trong ciphertext
    freqs = Counter(text)
    n = len(text)     # Tổng số ký tự
    # Công thức Entropy: H = - Σ (p * log2(p))
    # p = f / n  (f: tần suất ký tự)
    return -sum((f/n)*math.log2(f/n) for f in freqs.values()) if n > 0 else 0

# Xác suất trùng ký tự - ic
def index_of_coincidence(text):
    n = len(text)
    freqs = Counter(text)    # Đếm tần suất từng ký tự
    # Công thức IC: Σ f*(f-1) / (n*(n-1))
    # IC cao → có cấu trúc (ngôn ngữ tự nhiên)
    # IC thấp → random (XOR)
    return sum(f*(f-1) for f in freqs.values()) / (n*(n-1)+1e-9)

# Lệch so với phân bố đều - chi
def chi_square(text):
    # Giá trị kỳ vọng mỗi ký tự nếu phân bố đều
    expected = len(text)/26 if len(text)>0 else 1
    freqs = Counter(text)     # Đếm tần suất
    # Công thức: χ² = Σ ((O - E)² / E)
    # O = observed (tần suất thực tế)
    # E = expected (tần suất kỳ vọng)
    return sum((freqs.get(chr(97+i),0)-expected)**2/expected for i in range(26))


# Min Chi-square sau khi dịch
def min_chi_after_shift(text):
    if len(text) == 0:
        return 0
    scores = []
    for k in range(26):
        shifted = ''.join(chr((ord(c)-97-k) % 26 + 97) for c in text)
        scores.append(chi_square(shifted))
    return min(scores)

# IC trung bình khi dịch
def avg_shift_ic(text, max_k=12):
    n = len(text)
    if n < max_k:
        return 0
    scores = []
    for k in range(2, max_k):
        match = sum(1 for i in range(n-k) if text[i] == text[i+k])
        scores.append(match / (n-k))
    return sum(scores) / len(scores)
    
# Digram lặp
def repeated_digrams(text):
    if len(text) < 2:
        return 0
    pairs = [text[i:i+2] for i in range(len(text)-1)]
    freqs = Counter(pairs)
    return sum(1 for v in freqs.values() if v > 1)

# Phương sai entropy theo block
def block_entropy_variance(text, block_size=20):
    if len(text) < block_size:
        return 0
    ents = []
    for i in range(0, len(text), block_size):
        block = text[i:i+block_size]
        if len(block) > 5:
            ents.append(entropy(block))
    return np.var(ents) if len(ents) > 1 else 0
# Diagram entropy
def digram_entropy(text):
    if len(text) < 4:
        return 0

    digrams = [text[i:i+2] for i in range(len(text)-1)]
    freq = Counter(digrams)
    n = sum(freq.values())

    return -sum((f/n) * math.log2(f/n) for f in freq.values())

def extract_features(df):
    feats = []  # danh sách chứa feature vector của từng ciphertext

    # Lặp qua từng ciphertext trong dataframe
    for ct in df['ciphertext']:

        # Giữ lại CHỈ chữ cái a-z (loại bỏ số, hex, ký tự đặc biệt)
        t = clean_text_only_letters(ct)

        # Tạo bộ features cho 1 ciphertext
        f = {
            "entropy": entropy(t),                      # 1. Entropy
            "ic": index_of_coincidence(t),              # 2. Index of Coincidence
            "chi": chi_square(t),                       # 3. Chi-square
            "length": len(t),                            # 4. Độ dài
            "min_chi_after_shift": min_chi_after_shift(t),
            "avg_shift_ic": avg_shift_ic(t),
            "repeated_digrams": repeated_digrams(t),
            "block_entropy_variance": block_entropy_variance(t),
            "digram_entropy": digram_entropy(t)
        }

        # 5. Tần suất từng ký tự a–z
        for i in range(26):
            char = chr(97 + i)
            f[f"freq_{char}"] = t.count(char) / (len(t) + 1e-9)

        feats.append(f)

    return pd.DataFrame(feats)
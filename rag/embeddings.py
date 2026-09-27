import numpy as np
import math
import hashlib
from typing import List

class EmbeddingModel:
    """Deterministic high-dimensional embedding model using TF-IDF / Hash projections."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    def _hash_word(self, word: str) -> np.ndarray:
        vec = np.zeros(self.dimension, dtype=np.float32)
        h = int(hashlib.md5(word.lower().encode('utf-8')).hexdigest(), 16)
        for i in range(4):
            idx = (h >> (i * 16)) % self.dimension
            sign = 1.0 if (h >> (i * 16 + 8)) % 2 == 0 else -1.0
            vec[idx] += sign
        return vec

    def embed_text(self, text: str) -> np.ndarray:
        words = [w.strip(".,!?;:\"'()[]{}") for w in text.lower().split() if len(w) > 2]
        if not words:
            return np.zeros(self.dimension, dtype=np.float32)

        vector = np.zeros(self.dimension, dtype=np.float32)
        for word in words:
            vector += self._hash_word(word)

        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector

    def embed_batch(self, texts: List[str]) -> List[np.ndarray]:
        return [self.embed_text(t) for t in texts]

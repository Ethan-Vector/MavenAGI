from __future__ import annotations

import os
import re
from dataclasses import dataclass
from math import sqrt
from typing import Dict, Iterable, List, Tuple


def _tokenize(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r"[^a-z0-9_\s-]+", " ", text)
    return [t for t in text.split() if t]


def _tf(tokens: Iterable[str]) -> Dict[str, int]:
    d: Dict[str, int] = {}
    for t in tokens:
        d[t] = d.get(t, 0) + 1
    return d


def _cosine(a: Dict[str, int], b: Dict[str, int]) -> float:
    dot = 0.0
    na = 0.0
    nb = 0.0
    for k, va in a.items():
        na += va * va
        vb = b.get(k)
        if vb is not None:
            dot += va * vb
    for vb in b.values():
        nb += vb * vb
    if na <= 0 or nb <= 0:
        return 0.0
    return dot / (sqrt(na) * sqrt(nb))


@dataclass(frozen=True)
class Hit:
    doc_id: str
    score: float
    snippet: str


class TinyIndex:
    def __init__(self) -> None:
        self._docs: Dict[str, str] = {}
        self._vecs: Dict[str, Dict[str, int]] = {}

    def add(self, doc_id: str, text: str) -> None:
        self._docs[doc_id] = text
        self._vecs[doc_id] = _tf(_tokenize(text))

    def search(self, query: str, k: int = 5) -> List[Hit]:
        qv = _tf(_tokenize(query))
        scored: List[Tuple[str, float]] = []
        for doc_id, dv in self._vecs.items():
            scored.append((doc_id, _cosine(qv, dv)))
        scored.sort(key=lambda x: x[1], reverse=True)
        hits: List[Hit] = []
        for doc_id, score in scored[:k]:
            text = self._docs[doc_id]
            snippet = text[:240].replace("\n", " ").strip()
            hits.append(Hit(doc_id=doc_id, score=float(score), snippet=snippet))
        return hits

    @staticmethod
    def from_docs_dir(path: str) -> "TinyIndex":
        idx = TinyIndex()
        for root, _, files in os.walk(path):
            for fn in files:
                if not fn.lower().endswith(".md"):
                    continue
                full = os.path.join(root, fn)
                with open(full, "r", encoding="utf-8") as f:
                    idx.add(os.path.relpath(full, path), f.read())
        return idx

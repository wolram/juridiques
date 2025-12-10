import os
from typing import List, Dict

# RAG simples: busca por substring nos documentos da pasta docs/
DOCS_PATH = os.path.join(os.path.dirname(__file__), "..", "docs")


def _read_docs() -> List[Dict[str, str]]:
    docs = []
    base = os.path.abspath(DOCS_PATH)
    if not os.path.isdir(base):
        return docs
    for fname in os.listdir(base):
        path = os.path.join(base, fname)
        if not os.path.isfile(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            text = ""
        docs.append({"id": fname, "text": text, "path": path})
    return docs


def retrieve(query: str, top_k: int = 3) -> List[Dict[str, str]]:
    """Busca simples por ocorrências do query nos documentos e retorna top_k resultados com score."""
    docs = _read_docs()
    hits = []
    q = query.lower()
    for d in docs:
        cnt = d["text"].lower().count(q) if q else 0
        if cnt > 0:
            snippet_start = d["text"].lower().find(q)
            start = max(0, snippet_start - 80)
            end = min(len(d["text"]), snippet_start + 160)
            snippet = d["text"][start:end].replace("\n", " ")
            hits.append({"id": d["id"], "path": d["path"], "snippet": snippet, "score": float(cnt)})
    hits.sort(key=lambda x: x["score"], reverse=True)
    return hits[:top_k]

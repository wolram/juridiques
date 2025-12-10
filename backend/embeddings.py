from typing import List, Optional
import logging

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_SB = True
except Exception:
    HAS_SB = False


logger = logging.getLogger(__name__)


class EmbeddingsClient:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        if HAS_SB:
            try:
                self.model = SentenceTransformer(model_name)
            except Exception as e:
                logger.warning("Falha ao carregar SentenceTransformer: %s", e)

    def embed_texts(self, texts: List[str]):
        if self.model:
            return self.model.encode(texts, convert_to_numpy=True)
        # Fallback simples: hashes -> vetor pequeno
        import hashlib
        import numpy as np

        def hvec(s: str):
            h = hashlib.sha256(s.encode("utf-8")).digest()
            arr = np.frombuffer(h[:64], dtype='u1').astype('float32')
            arr = arr / 255.0
            return arr

        return np.stack([hvec(t) for t in texts])


emb_client = EmbeddingsClient()


def embed_text(text: str):
    vecs = emb_client.embed_texts([text])
    return vecs[0]

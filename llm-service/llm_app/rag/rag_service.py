import json
import faiss
import numpy as np
from pathlib import Path

from llm_app.rag.embedding_service import EmbeddingService


BASE_DIR = Path(__file__).resolve().parent.parent
VECTOR_DIR = BASE_DIR / "vector_store"


class RAGService:

    @staticmethod
    def retrieve(query: str, top_k: int = 3):

        index = faiss.read_index(
            str(VECTOR_DIR / "faiss.index")
        )

        with open(
            VECTOR_DIR / "chunks.json",
            "r",
            encoding="utf-8"
        ) as f:
            chunks = json.load(f)

        query_vector = EmbeddingService.encode([query])
        query_vector = np.array(query_vector, dtype=np.float32)

        scores, indices = index.search(query_vector, top_k)

        results = []

        for score, idx in zip(scores[0], indices[0]):
            results.append({
                "id": f"chunk_{idx}",
                "text": chunks[idx],
                "score": float(score),
                "index": int(idx),
                "score_type": "faiss_distance"
            })

        return results
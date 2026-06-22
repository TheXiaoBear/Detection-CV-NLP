from pathlib import Path
import json
import faiss
import numpy as np

from llm_app.rag.embedding_service import EmbeddingService
from llm_app.rag.chunk_service import ChunkService


BASE_DIR = Path(__file__).resolve().parent.parent

KNOWLEDGE_DIR = BASE_DIR / "knowledge"

VECTOR_DIR = BASE_DIR / "vector_store"


class FaissIndexBuilder:

    @staticmethod
    def build():

        all_chunks = []

        for file in KNOWLEDGE_DIR.glob("*.md"):

            with open(
                file,
                "r",
                encoding="utf-8"
            ) as f:

                text = f.read()

            chunks = (
                ChunkService.split(text)
            )

            all_chunks.extend(chunks)

        if not all_chunks:
            return

        vectors = (
            EmbeddingService.encode(
                all_chunks
            )
        )

        vectors = np.array(
            vectors,
            dtype=np.float32
        )

        dimension = vectors.shape[1]

        index = faiss.IndexFlatIP(
            dimension
        )

        index.add(vectors)

        VECTOR_DIR.mkdir(
            exist_ok=True
        )

        faiss.write_index(
            index,
            str(
                VECTOR_DIR / "faiss.index"
            )
        )

        with open(
            VECTOR_DIR / "chunks.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                all_chunks,
                f,
                ensure_ascii=False,
                indent=2
            )

        print(
            f"索引构建完成，共 {len(all_chunks)} 个chunk"
        )
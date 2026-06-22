from sentence_transformers import SentenceTransformer


class EmbeddingService:

    model = SentenceTransformer(
        "BAAI/bge-small-zh-v1.5"
    )

    @classmethod
    def encode(
        cls,
        texts
    ):
        return cls.model.encode(
            texts,
            normalize_embeddings=True
        )
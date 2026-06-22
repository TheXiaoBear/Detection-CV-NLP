from llm_app.rag.rag_service import (
    RAGService
)

result = (
    RAGService.retrieve(
        "检测结果置信度较低"
    )
)

for item in result:
    print(item)
    print("=" * 50)
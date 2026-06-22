import re


class CitationParser:

    @staticmethod
    def extract_chunk_ids(text: str):
        """
        从报告中提取 [chunk_x]
        """
        return re.findall(r"\[chunk_\d+\]", text)

    @staticmethod
    def build_citations(report_text: str, rag_results: list):

        used_ids = CitationParser.extract_chunk_ids(report_text)

        citation_map = {
            item["id"]: item
            for item in rag_results
        }

        citations = []

        for cid in used_ids:

            if cid in citation_map:

                citations.append({
                    "chunk_id": cid,
                    "text": citation_map[cid]["text"],
                    "score": citation_map[cid]["score"]
                })

        return citations
"""Retrieve relevant IELTS essay chunks from FAISS index."""

import pickle
from pathlib import Path
from typing import List, Dict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class IELTSRetriever:
    """RAG retriever for IELTS essay corpus."""

    def __init__(self, index_dir: str, model_name: str = "all-MiniLM-L6-v2"):
        self.index_dir = Path(index_dir)
        self.model = SentenceTransformer(model_name)

        # Load index
        index_path = self.index_dir / "essays.index"
        if not index_path.exists():
            raise FileNotFoundError(f"Index not found: {index_path}. Run indexer.py first.")

        self.index = faiss.read_index(str(index_path))

        # Load chunk metadata
        with open(self.index_dir / "chunks.pkl", "rb") as f:
            self.chunks = pickle.load(f)

    def search(
        self,
        query: str,
        top_k: int = 5,
        task_type: str = None,       # "task1" or "task2"
        min_score: float = None,     # minimum band score for samples
        max_score: float = None,     # maximum band score for samples
        is_question: bool = None,    # filter questions vs samples
    ) -> List[Dict]:
        """Search for relevant chunks with optional filters."""

        # Build query embedding
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_embedding)

        # Search
        scores, indices = self.index.search(query_embedding, top_k * 3)  # Over-fetch for filtering

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            chunk = self.chunks[idx]

            # Apply filters
            if task_type and chunk["task_type"] != task_type:
                continue
            if is_question is not None and chunk["is_question"] != is_question:
                continue
            if min_score is not None and chunk["score"] is not None and chunk["score"] < min_score:
                continue
            if max_score is not None and chunk["score"] is not None and chunk["score"] > max_score:
                continue

            results.append({
                "score": float(score),
                "text": chunk["raw_text"],
                "file": chunk["file"],
                "section": chunk["section"],
                "task_type": chunk["task_type"],
                "is_question": chunk["is_question"],
                "band_score": chunk["score"],
                "metadata": chunk["metadata"],
            })

            if len(results) >= top_k:
                break

        return results

    def get_context_string(self, results: List[Dict]) -> str:
        """Format search results as context for LLM."""
        lines = []
        for i, r in enumerate(results, 1):
            source = "Question" if r["is_question"] else f"Sample (Band {r['band_score']})"
            lines.append(f"[{i}] {source} | {r['section']}")
            lines.append(r["text"])
            lines.append("")
        return "\n".join(lines)


if __name__ == "__main__":
    import sys

    index_dir = sys.argv[1] if len(sys.argv) > 1 else "../index"
    retriever = IELTSRetriever(index_dir)

    # Test queries
    test_queries = [
        "table showing population changes over time",
        "opinion essay about public services",
        "how to describe percentage changes in Task 1",
        "Band 7 essay about water",
    ]

    for q in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: {q}")
        print("="*60)
        results = retriever.search(q, top_k=3)
        for r in results:
            print(f"\n[{r['task_type']}] Score: {r['score']:.3f} | {r['section']}")
            print(r["text"][:300] + "...")

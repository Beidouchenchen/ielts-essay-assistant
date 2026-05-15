"""Main RAG engine for IELTS essay assistant."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from retriever import IELTSRetriever


class IELTSRAGEngine:
    """High-level RAG engine for IELTS essay tasks."""

    def __init__(self, index_dir: str = "../index"):
        self.retriever = IELTSRetriever(index_dir)

    def find_similar_questions(self, query: str, task_type: str = None, top_k: int = 3) -> str:
        """Find similar questions from the corpus."""
        results = self.retriever.search(
            query,
            top_k=top_k,
            task_type=task_type,
            is_question=True,
        )
        return self.retriever.get_context_string(results)

    def find_sample_essays(
        self,
        query: str,
        task_type: str = None,
        min_score: float = None,
        max_score: float = None,
        top_k: int = 5,
    ) -> str:
        """Find sample essays matching criteria."""
        results = self.retriever.search(
            query,
            top_k=top_k,
            task_type=task_type,
            is_question=False,
            min_score=min_score,
            max_score=max_score,
        )
        return self.retriever.get_context_string(results)

    def get_reference_for_writing(
        self,
        topic: str,
        task_type: str,
        target_band: float = 7.0,
        top_k: int = 3,
    ) -> str:
        """Get reference materials for a writing task."""
        query = f"{topic} {task_type} IELTS essay"

        # Get similar questions
        questions = self.retriever.search(
            query,
            top_k=2,
            task_type=task_type,
            is_question=True,
        )

        # Get high-scoring samples
        samples = self.retriever.search(
            query,
            top_k=top_k,
            task_type=task_type,
            is_question=False,
            min_score=target_band - 1.0,
            max_score=target_band + 1.0,
        )

        # Also get lower score samples for comparison
        weak_samples = self.retriever.search(
            query,
            top_k=2,
            task_type=task_type,
            is_question=False,
            max_score=target_band - 1.5,
        )

        all_results = questions + samples + weak_samples
        return self.retriever.get_context_string(all_results)


def interactive_mode():
    """CLI interactive mode."""
    engine = IELTSRAGEngine()

    print("="*60)
    print("IELTS Essay RAG Engine")
    print("Commands: q=quit, t1=Task1, t2=Task2")
    print("="*60)

    while True:
        query = input("\nQuery: ").strip()
        if not query:
            continue
        if query.lower() == "q":
            break

        task_type = None
        if query.lower() == "t1":
            task_type = "task1"
            query = input("  Task 1 query: ")
        elif query.lower() == "t2":
            task_type = "task2"
            query = input("  Task 2 query: ")

        results = engine.retriever.search(query, task_type=task_type, top_k=5)

        print(f"\nFound {len(results)} results:")
        for r in results:
            badge = "[Q]" if r["is_question"] else f"[B{r['band_score']}]"
            print(f"  {badge} {r['section']} (score: {r['score']:.3f})")
            print(f"    {r['text'][:200]}...")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        # Demo
        engine = IELTSRAGEngine()

        print("\n" + "="*60)
        print("Demo 1: Find similar questions")
        print("="*60)
        print(engine.find_similar_questions("population changes in cities", task_type="task1"))

        print("\n" + "="*60)
        print("Demo 2: Find sample essays")
        print("="*60)
        print(engine.find_sample_essays("water public services", task_type="task2", min_score=6.0))

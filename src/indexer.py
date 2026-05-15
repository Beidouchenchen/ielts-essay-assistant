"""Build FAISS index from IELTS essay corpus."""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

import faiss
import numpy as np
import yaml
from sentence_transformers import SentenceTransformer


def extract_chunks_from_md(filepath: str) -> List[Dict]:
    """Split a markdown file into semantic chunks with metadata."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    chunks = []
    base_name = Path(filepath).stem
    test_dir = Path(filepath).parent
    meta_path = test_dir / "metadata.yaml"

    # Load metadata
    metadata = {}
    if meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            metadata = yaml.safe_load(f)

    # Detect task type and score from filename
    task_type = "task1" if "task1" in base_name else "task2"
    is_question = "question" in base_name

    score_match = re.search(r"sample-(\d\.\d)", base_name)
    score = float(score_match.group(1)) if score_match else None

    # Split by major sections (## headers)
    sections = re.split(r"\n## ", content)

    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue

        # Extract section title if present
        lines = section.split("\n")
        section_title = lines[0].strip("# ") if i > 0 else "overview"
        section_body = "\n".join(lines[1:]).strip()

        if len(section_body) < 30:
            continue

        # Build rich context for embedding
        context_parts = [f"[{task_type.upper()}]"]
        if is_question:
            context_parts.append("[QUESTION]")
        else:
            context_parts.append(f"[SAMPLE][BAND:{score}]")

        # Add metadata context
        if task_type == "task1" and metadata.get("question_types", {}).get("task1"):
            t1 = metadata["question_types"]["task1"]
            context_parts.append(f"[CHART:{t1.get('chart_type', 'unknown')}]")
            context_parts.append(f"[TOPIC:{t1.get('topic', 'unknown')}]")
        elif task_type == "task2" and metadata.get("question_types", {}).get("task2"):
            t2 = metadata["question_types"]["task2"]
            context_parts.append(f"[TYPE:{t2.get('type', 'unknown')}]")
            context_parts.append(f"[TOPIC:{t2.get('topic', 'unknown')}]")

        context_parts.append(f"[SECTION:{section_title}]")

        full_text = " ".join(context_parts) + "\n" + section_body

        chunks.append({
            "text": full_text,
            "raw_text": section_body,
            "file": filepath,
            "section": section_title,
            "task_type": task_type,
            "is_question": is_question,
            "score": score,
            "metadata": metadata,
        })

    return chunks


def build_index(data_dir: str, index_dir: str, model_name: str = "all-MiniLM-L6-v2") -> Tuple[faiss.Index, List[Dict]]:
    """Build FAISS index from all markdown files."""
    data_path = Path(data_dir)
    index_path = Path(index_dir)
    index_path.mkdir(parents=True, exist_ok=True)

    # Collect all chunks
    all_chunks = []
    for md_file in data_path.rglob("*.md"):
        chunks = extract_chunks_from_md(str(md_file))
        all_chunks.extend(chunks)

    if not all_chunks:
        raise ValueError(f"No markdown files found in {data_dir}")

    print(f"Found {len(all_chunks)} chunks from corpus")

    # Load embedding model
    model = SentenceTransformer(model_name)
    dim = model.get_embedding_dimension()

    # Generate embeddings
    texts = [chunk["text"] for chunk in all_chunks]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    # Build FAISS index
    index = faiss.IndexFlatIP(dim)  # Inner product = cosine similarity after normalization
    index.add(embeddings)

    # Save index
    faiss.write_index(index, str(index_path / "essays.index"))

    # Save chunk metadata
    import pickle
    with open(index_path / "chunks.pkl", "wb") as f:
        pickle.dump(all_chunks, f)

    print(f"Index saved: {index_path / 'essays.index'}")
    print(f"Dimension: {dim}, Vectors: {index.ntotal}")

    return index, all_chunks


if __name__ == "__main__":
    import sys

    data_dir = sys.argv[1] if len(sys.argv) > 1 else "../data"
    index_dir = sys.argv[2] if len(sys.argv) > 2 else "../index"

    build_index(data_dir, index_dir)

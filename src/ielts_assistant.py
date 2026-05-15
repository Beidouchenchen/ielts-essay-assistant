"""IELTS Essay Assistant - Dynamic mode loading with score-spectrum RAG."""

import argparse
import hashlib
import io
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Force UTF-8 on Windows
if sys.platform == "win32" and sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

sys.path.insert(0, str(Path(__file__).parent))

import yaml
from retriever import IELTSRetriever


class RAGCache:
    """Cache RAG retrieval results to avoid redundant searches."""

    def __init__(self, cache_dir: str = None, index_dir: str = "../index"):
        self.cache_dir = Path(cache_dir) if cache_dir else Path(__file__).parent / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "rag_cache.json"
        self.index_dir = Path(index_dir)
        self._cache: Dict = self._load()

    def _load(self) -> Dict:
        if self.cache_file.exists():
            try:
                return json.loads(self.cache_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                return {"index_mtime": 0, "entries": {}}
        return {"index_mtime": 0, "entries": {}}

    def _save(self):
        self.cache_file.write_text(json.dumps(self._cache, ensure_ascii=False), encoding="utf-8")

    def _index_mtime(self) -> float:
        index_path = self.index_dir / "essays.index"
        return index_path.stat().st_mtime if index_path.exists() else 0

    def _make_key(self, query: str, strategy: str, task_type: str) -> str:
        raw = f"{query}|{strategy}|{task_type}"
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, query: str, strategy: str, task_type: str) -> Optional[str]:
        """Return cached context if valid, else None."""
        mtime = self._index_mtime()
        if self._cache.get("index_mtime") != mtime:
            self._cache = {"index_mtime": mtime, "entries": {}}
            return None
        key = self._make_key(query, strategy, task_type)
        return self._cache["entries"].get(key)

    def put(self, query: str, strategy: str, task_type: str, context: str):
        """Store context in cache."""
        mtime = self._index_mtime()
        if self._cache.get("index_mtime") != mtime:
            self._cache = {"index_mtime": mtime, "entries": {}}
        key = self._make_key(query, strategy, task_type)
        self._cache["entries"][key] = context
        self._save()


class PromptMode:
    """Represents a single prompt mode loaded from .md file."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.name = filepath.stem
        self.frontmatter: Dict = {}
        self.prompt_text = ""
        self._parse()

    def _parse(self):
        """Parse YAML frontmatter + markdown body."""
        content = self.filepath.read_text(encoding="utf-8")

        # Extract frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    self.frontmatter = yaml.safe_load(parts[1]) or {}
                except Exception:
                    self.frontmatter = {}
                self.prompt_text = parts[2].strip()
            else:
                self.prompt_text = content
        else:
            self.prompt_text = content

    @property
    def mode(self) -> str:
        return self.frontmatter.get("mode", self.name)

    @property
    def description(self) -> str:
        return self.frontmatter.get("description", "")

    @property
    def triggers(self) -> List[str]:
        return self.frontmatter.get("triggers", [])

    @property
    def rag_strategy(self) -> str:
        return self.frontmatter.get("rag_strategy", "all")

    def match(self, text: str) -> float:
        """Return match score (0-1) based on trigger keywords."""
        text_lower = text.lower()
        for trigger in self.triggers:
            if trigger.lower() in text_lower:
                return 1.0
        return 0.0


class IELTSAssistant:
    """High-level assistant with dynamic mode loading and score-spectrum RAG."""

    def __init__(self, index_dir: str = "../index"):
        self.retriever = IELTSRetriever(index_dir)
        self.cache = RAGCache(index_dir=index_dir)
        self.prompts_dir = Path(__file__).parent / "prompts"
        self.modes: Dict[str, PromptMode] = {}
        self._load_modes()

    def _load_modes(self):
        """Dynamically load all prompt modes from prompts/ directory."""
        for md_file in sorted(self.prompts_dir.glob("*.md")):
            mode = PromptMode(md_file)
            self.modes[mode.mode] = mode

    def list_modes(self) -> List[Dict]:
        """Return list of available modes for skill discovery."""
        return [
            {
                "mode": m.mode,
                "description": m.description,
                "triggers": m.triggers,
                "rag_strategy": m.rag_strategy,
            }
            for m in self.modes.values()
        ]

    def detect_mode(self, text: str) -> Optional[PromptMode]:
        """Detect mode from natural language input."""
        best_mode = None
        best_score = 0.0

        for mode in self.modes.values():
            score = mode.match(text)
            if score > best_score:
                best_score = score
                best_mode = mode

        return best_mode

    def _retrieve_spectrum(self, query: str, task_type: str = None, top_k: int = 8) -> str:
        """Retrieve mixed score spectrum to avoid overfitting."""
        results = []

        # High score samples (8+)
        high = self.retriever.search(
            query, task_type=task_type, is_question=False,
            min_score=8.0, top_k=2
        )
        results.extend(high)

        # Mid score samples (6.5-7.5)
        mid = self.retriever.search(
            query, task_type=task_type, is_question=False,
            min_score=6.5, max_score=7.5, top_k=2
        )
        results.extend(mid)

        # Low score samples (5-6)
        low = self.retriever.search(
            query, task_type=task_type, is_question=False,
            max_score=6.0, top_k=2
        )
        results.extend(low)

        # Questions
        questions = self.retriever.search(
            query, task_type=task_type, is_question=True, top_k=2
        )
        results.extend(questions)

        return self.retriever.get_context_string(results)

    def _retrieve_high_only(self, query: str, task_type: str = None, top_k: int = 5) -> str:
        """Retrieve only high-scoring samples."""
        results = self.retriever.search(
            query, task_type=task_type, is_question=False,
            min_score=7.5, top_k=top_k
        )
        return self.retriever.get_context_string(results)

    def _retrieve_all(self, query: str, task_type: str = None, top_k: int = 10) -> str:
        """Retrieve all relevant materials."""
        results = self.retriever.search(query, task_type=task_type, top_k=top_k)
        return self.retriever.get_context_string(results)

    def _get_context(self, query: str, mode: PromptMode, task_type: str = None) -> str:
        """Get context based on mode's RAG strategy, with caching."""
        strategy = mode.rag_strategy

        # Check cache first
        cached = self.cache.get(query, strategy, task_type or "auto")
        if cached is not None:
            return cached

        # Retrieve fresh results
        if strategy == "mixed_scores":
            context = self._retrieve_spectrum(query, task_type)
        elif strategy == "high_only":
            context = self._retrieve_high_only(query, task_type)
        elif strategy == "all":
            context = self._retrieve_all(query, task_type)
        else:
            context = self._retrieve_all(query, task_type)

        # Cache the result
        self.cache.put(query, strategy, task_type or "auto", context)
        return context

    def run_mode(self, mode_name: str, content: str, question: str = None, task_type: str = None) -> str:
        """Run a specific mode with given input."""
        if mode_name not in self.modes:
            available = ", ".join(self.modes.keys())
            raise ValueError(f"Unknown mode: {mode_name}. Available: {available}")

        mode = self.modes[mode_name]
        prompt_template = mode.prompt_text

        # Detect task type for essay-related modes
        if task_type is None and len(content.split()) > 200:
            task_type = "task2"
        elif task_type is None:
            task_type = "task1"

        # Retrieve context
        query = question or content[:100]
        context = self._get_context(query, mode, task_type)

        # Build full prompt
        return f"""{prompt_template}

---

## 用户输入

**任务类型：** {task_type.upper()}

**题目（如有）：**
{question or "[未提供]"}

**内容：**
{content}

---

## 参考资料库检索结果

{context}

---

请根据以上信息，按照 {mode.description} 的输出格式，生成回答。
**注意：** 参考范文仅作为评分标准和技巧参考，不要直接模仿其具体表达，保持独立判断。
"""


def main():
    parser = argparse.ArgumentParser(description="IELTS Essay Assistant")
    parser.add_argument(
        "action",
        choices=["run", "list", "detect"],
        help="Action: run(执行模式), list(列出所有模式), detect(检测意图)"
    )
    parser.add_argument("--mode", "-m", help="Mode name to run")
    parser.add_argument("--input", "-i", help="Input file path")
    parser.add_argument("--text", "-t", help="Direct input text")
    parser.add_argument("--question", "-q", help="Question prompt")
    parser.add_argument("--task", choices=["task1", "task2"], help="Task type")
    parser.add_argument("--index-dir", default="../index", help="FAISS index directory")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    assistant = IELTSAssistant(args.index_dir)

    if args.action == "list":
        import json
        modes = assistant.list_modes()
        print(json.dumps(modes, ensure_ascii=False, indent=2))
        return

    if args.action == "detect":
        text = args.text or ""
        if not text and args.input:
            text = Path(args.input).read_text(encoding="utf-8")
        mode = assistant.detect_mode(text)
        if mode:
            print(f"Detected mode: {mode.mode}")
            print(f"Description: {mode.description}")
            print(f"Triggers: {', '.join(mode.triggers)}")
        else:
            print("No mode detected")
        return

    # action == "run"
    if not args.mode:
        print("Error: --mode required for run action", file=sys.stderr)
        sys.exit(1)

    content = ""
    if args.text:
        content = args.text
    elif args.input:
        content = Path(args.input).read_text(encoding="utf-8")

    result = assistant.run_mode(args.mode, content, args.question, args.task)

    if args.output:
        Path(args.output).write_text(result, encoding="utf-8")
        print(f"Output saved to: {args.output}")
    else:
        print(result)


if __name__ == "__main__":
    main()

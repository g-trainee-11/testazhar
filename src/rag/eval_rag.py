"""RAG Evaluation harness for search_kb function using OpenAI and simple faithfulness check."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

from openai import OpenAI

# Add src directory to path for relative imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from rag.kb_search import search_kb

MODEL_NAME = "gpt-4o-mini"


def _get_openai_client() -> OpenAI:
    """Get OpenAI client with fallback to GITHUB_TOKEN if OPENAI_API_KEY not set."""
    github_token = os.getenv("GITHUB_TOKEN")
    openai_key = os.getenv("OPENAI_API_KEY")

    if github_token:
        return OpenAI(
            api_key=github_token, 
            base_url="https://models.inference.ai.azure.com"
        )

    if openai_key:
        return OpenAI(api_key=openai_key)

    raise RuntimeError(
        "No API key found. Set GITHUB_TOKEN or OPENAI_API_KEY in the environment."
    )


def _generate_answer(client: OpenAI, query: str, contexts: list[str]) -> str:
    """Generate answer using OpenAI based on retrieved context."""
    prompt = (
        "Use only the provided context to answer the question. "
        "If the answer cannot be found in the context, reply with 'I don't know'.\n\n"
        "Context:\n"
        f"{chr(10).join(contexts)}\n\n"
        f"Question: {query}\nAnswer:"
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.01,
    )
    return response.choices[0].message.content


def _build_context(entry: dict[str, Any]) -> str:
    """Build context string from KB entry."""
    title = entry.get("title", "")
    description = entry.get("description", "")
    return f"{title}: {description}".strip()


def _check_faithfulness(answer: str, reference: str) -> float:
    """Simple faithfulness check: score 1.0 if reference found in answer, else 0.0."""
    return 1.0 if reference.lower() in answer.lower() else 0.0


def run_rag_eval() -> None:
    """Run faithfulness evaluation on search_kb function."""
    client = _get_openai_client()

    test_cases = [
        {"query": "how many people can join chess club", "reference": "12"},
        {"query": "when does basketball practice run", "reference": "Monday"},
        {"query": "morning run maximum participants", "reference": "30"},
        {"query": "is there a daily activity", "reference": "Daily"},
    ]

    scores: list[float] = []
    results_log: list[dict[str, Any]] = []

    print("Running RAG faithfulness evaluation for search_kb...\n")

    for tc in test_cases:
        query = tc["query"]
        reference = tc["reference"]
        print(f"{'='*60}")
        print(f"Query: {query}")
        print(f"Expected: {reference}")

        # Search KB
        entries = search_kb(query, top_k=3)
        contexts = [_build_context(entry) for entry in entries]
        print(f"Retrieved contexts: {len(entries)}")

        # Generate answer
        answer = _generate_answer(client, query, contexts)
        print(f"Answer: {answer}")

        # Check faithfulness
        score = _check_faithfulness(answer, reference)
        scores.append(score)
        print(f"Faithful: {score == 1.0} (score: {score:.2f})")

        results_log.append({
            "query": query,
            "reference": reference,
            "answer": answer,
            "contexts": contexts,
            "faithfulness_score": score
        })

    avg_score = sum(scores) / len(scores) if scores else 0.0
    print(f"\n{'='*60}")
    print(f"Average Faithfulness Score: {avg_score:.4f}")

    # Save results
    results_file = Path(__file__).parent / "eval_results.json"
    with open(results_file, "w") as f:
        json.dump({
            "model": MODEL_NAME,
            "average_faithfulness": avg_score,
            "test_cases": results_log,
            "threshold": 0.85,
            "passed": avg_score >= 0.85
        }, f, indent=2)

    print(f"Results saved to {results_file}")

    if avg_score < 0.85:
        print(f"\nERROR: Faithfulness score {avg_score:.4f} below threshold 0.85")
        sys.exit(1)

    print("\nSUCCESS: Faithfulness threshold met!")
    sys.exit(0)


if __name__ == "__main__":
    run_rag_eval()

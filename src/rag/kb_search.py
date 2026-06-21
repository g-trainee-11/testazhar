from __future__ import annotations

import json
import re
from pathlib import Path
from typing import List

KB_PATH = Path(__file__).parent / "activities_kb.json"

# Common stop words to filter
STOP_WORDS = {
    "is", "are", "am", "be", "been", "being",
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "by", "with", "as", "from", "about", "was", "were", "do", "does",
    "did", "will", "would", "could", "should", "there", "that", "this", "it",
    "you", "i", "we", "they", "he", "she", "what", "which", "who", "when",
    "where", "why", "how", "no", "not", "if", "can", "has", "have", "had"
}


def search_kb(query: str, top_k: int = 3) -> List[dict]:
    """Search the activities knowledge base and return the top matching entries.

    The function loads entries from src/rag/activities_kb.json and ranks them by
    keyword overlap over title and description, filtering common stop words.
    """
    if not query:
        return []

    # Split query into terms and filter stop words
    terms = [term for term in re.split(r"\W+", query.lower()) 
             if term and term not in STOP_WORDS]
    if not terms:
        return []

    with KB_PATH.open("r", encoding="utf-8") as handle:
        entries = json.load(handle)

    scored_entries = []
    for entry in entries:
        title = entry.get("title", "")
        description = entry.get("description", "")
        text = f"{title} {description}".lower()
        score = sum(text.count(term) for term in terms)
        if score > 0:
            scored_entries.append((score, entry))

    scored_entries.sort(key=lambda item: (-item[0], item[1].get("title", "")))
    return [entry for _, entry in scored_entries[:top_k]]


if __name__ == "__main__":
    sample_queries = [
        "chess tournament",
        "art and sculpture",
        "basketball practice",
    ]

    for query in sample_queries:
        print(f"Query: {query}")
        results = search_kb(query)
        for result in results:
            print(f"- {result.get('title')} ({result.get('id')})")
        print()

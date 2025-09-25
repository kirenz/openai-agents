"""Hilfsfunktionen für ChromaDB und Embeddings."""

from __future__ import annotations

import textwrap
import uuid
from typing import Any, Dict, List, Optional

import chromadb
from chromadb.api.models import Collection
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from .settings import CHROMA_HOST, CHROMA_PORT, OPENAI_API_KEY


# Embedding-Funktion nutzt das OpenAI Responses-Modell für semantische Vektoren.
embedding_fn = OpenAIEmbeddingFunction(
    api_key=OPENAI_API_KEY,
    model_name="text-embedding-3-small",  # schnell & günstig; bei Bedarf 'text-embedding-3-large'
)

chroma_client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)


def get_wissensbasis_collection() -> Collection:
    """Gibt die standardisierte Chroma-Collection zurück."""
    return chroma_client.get_or_create_collection(
        name="wissensbasis",
        metadata={"hnsw:space": "cosine"},
        embedding_function=embedding_fn,
    )


def chunk_text(text: str, max_chars: int = 2000, overlap: int = 200) -> List[str]:
    """Einfache, sprachagnostische Chunking-Strategie mit Überlappung."""
    # Entferne doppelte Leerzeichen und Zeilenumbrüche, damit die Chunks kompakt bleiben.
    sanitized = " ".join(text.split())
    chunks: List[str] = []
    start = 0
    while start < len(sanitized):
        end = min(start + max_chars, len(sanitized))
        chunk = sanitized[start:end]
        chunks.append(chunk)
        start = max(0, end - overlap)
    return chunks


def add_documents(
    documents: List[str],
    metadatas: Optional[List[Dict[str, Any]]] = None,
    ids: Optional[List[str]] = None,
) -> None:
    """Speichert Dokumente inklusive optionaler Metadaten in Chroma."""
    collection = get_wissensbasis_collection()
    # Generiere stabile IDs, damit Chroma die Einträge verwalten kann.
    generated_ids = ids or [str(uuid.uuid4()) for _ in documents]
    collection.add(
        documents=documents,
        metadatas=metadatas or [{} for _ in documents],
        ids=generated_ids,
    )


def semantic_query(query_text: str, n_results: int = 4) -> Optional[List[Dict[str, Any]]]:
    """Führt eine semantische Suche aus und liefert strukturierte Treffer."""
    collection = get_wissensbasis_collection()
    if collection.count() == 0:
        return None

    response = collection.query(
        query_texts=[query_text],
        n_results=max(1, n_results),
        include=["documents", "metadatas", "distances"],
    )
    documents = response.get("documents", [[]])[0]
    metadatas = response.get("metadatas", [[]])[0]
    distances = response.get("distances", [[]])[0]

    results: List[Dict[str, Any]] = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        results.append({
            "document": doc,
            "metadata": meta or {},
            "distance": float(dist) if dist is not None else None,
        })
    return results


def format_query_results(results: Optional[List[Dict[str, Any]]]) -> str:
    """Bereitet Suchtreffer formatiert für Textausgaben auf."""
    if results is None:
        return "Die Wissensbasis ist leer."
    if not results:
        return "Keine passenden Ergebnisse gefunden."

    lines: List[str] = []
    for index, item in enumerate(results, start=1):
        meta = item.get("metadata", {})
        distance = item.get("distance")
        source = meta.get("source") or meta.get("entity") or meta.get("type") or "unbekannt"
        score = 1 - distance if distance is not None else 0.0
        preview = textwrap.shorten(item.get("document", ""), width=300, placeholder=" …")
        lines.append(f"[{index}] Quelle: {source} | Score≈{score:.3f}\n{preview}")
    return "\n\n".join(lines)

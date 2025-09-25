"""Tool-Implementierungen, die sowohl der Agent als auch die UI verwenden."""

from __future__ import annotations

import logging

import requests
from bs4 import BeautifulSoup

from agents import function_tool

from .vector_store import add_documents, chunk_text, format_query_results, semantic_query


logger = logging.getLogger(__name__)


def query_database_logic(query_text: str, n_results: int = 4) -> str:
    """Zentralisierte Semantik-Suche inklusive Formatierung."""
    # Agent & UI teilen sich diesen Pfad, damit beide dieselben Antworten liefern.
    results = semantic_query(query_text, n_results)
    return format_query_results(results)


@function_tool
def query_database(query_text: str, n_results: int = 4) -> str:
    """Durchsucht die Wissensbasis und liefert formatierte Treffer."""
    # Der Decorator meldet diese Funktion beim Agents SDK als Tool an.
    return query_database_logic(query_text, n_results)


def web_fetch_and_store_logic(url: str) -> str:
    """Ruft eine URL ab, chunked den Text und speichert ihn in Chroma."""
    try:
        logger.info("Starte Web-Fetch für %s", url)
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        # Wir ziehen Sichttext zusammen, damit keine HTML-Fragmente in Chroma landen.
        text = soup.get_text(separator="\n", strip=True)
        chunks = chunk_text(text, max_chars=1800, overlap=150)
        add_documents(
            documents=chunks,
            metadatas=[{"source": url, "type": "web"} for _ in chunks],
        )
        logger.info("Web-Fetch erfolgreich (%s Chunks)", len(chunks))
        return f"{len(chunks)} Text-Chunks von {url} gespeichert."
    except requests.exceptions.RequestException as exc:
        logger.warning("Web-Fetch fehlgeschlagen: %s", exc)
        hint = (
            "Fehler beim Abruf/Speichern: Netzwerkzugang nicht möglich oder URL nicht erreichbar."
        )
        return f"{hint} ({exc})"
    except Exception as exc:  # noqa: BLE001 - wir zeigen Fehler direkt an
        logger.exception("Unerwarteter Fehler beim Web-Fetch")
        return f"Fehler beim Abruf/Speichern: {exc}"


@function_tool
def web_fetch_and_store(url: str) -> str:
    """Wrapper für den Agents-SDK Decorator."""
    # So kann der Agent dieselbe Logik verwenden wie das UI.
    return web_fetch_and_store_logic(url)

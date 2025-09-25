"""Zentrale Konfiguration und Konstanten für den RAG-Agenten."""

from __future__ import annotations

import os

from dotenv import load_dotenv

# .env laden, damit lokale Entwicklungswerte (z. B. OPENAI_API_KEY) verfügbar sind.
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("Bitte OPENAI_API_KEY in .env oder Umgebung setzen.")

# Standard-Konfiguration für die lokal laufende Chroma-Instanz.
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

# Titel und Beschreibung werden sowohl im FastAPI-Docs-UI als auch in der Gradio-Oberfläche genutzt.
APP_TITLE = "RAG Agent (Agents SDK Responses + ChromaDB)"
APP_DESCRIPTION = (
    "API-Service mit Wissensbasis in Chroma und einem Recherche-Agenten (Responses API)."
)

"""App-Entrypoint für FastAPI + Gradio."""

from __future__ import annotations

import os

from rag_agent import create_app

app = create_app()


if __name__ == "__main__":  # pragma: no cover - manueller Start
    import uvicorn

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8080"))
    # Hinweis im Terminal, damit Nutzer direkt den UI-Link öffnen können.
    ui_hint = f"http://localhost:{port}/ui"
    print(f"Starte RAG-Agent – UI unter {ui_hint} erreichbar.")
    # Damit kann die App zusätzlich direkt via `python rag_agent_app.py` gestartet werden.
    uvicorn.run(app, host=host, port=port)

"""Factory zum Aufbau der FastAPI-Anwendung inklusive Gradio UI."""

from __future__ import annotations

from fastapi import FastAPI
from gradio.routes import mount_gradio_app

from .api import router as api_router
from .settings import APP_DESCRIPTION, APP_TITLE
from .ui import create_gradio_blocks


def create_app() -> FastAPI:
    """Erzeugt die FastAPI-Anwendung und hängt die Gradio-Oberfläche an."""
    app = FastAPI(title=APP_TITLE, description=APP_DESCRIPTION)
    app.include_router(api_router)

    rag_ui = create_gradio_blocks()
    # Die Gradio-Oberfläche wird unter /ui bereitgestellt, während FastAPI die API-Endpunkte liefert.
    app = mount_gradio_app(app, rag_ui, path="/ui")
    return app

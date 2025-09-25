"""Gradio-Oberfläche für das Testen des Agenten."""

from __future__ import annotations

from typing import Any, List, Tuple

import gradio as gr

from .agent import clear_conversation, run_agent_turn
from .seeding import seed_example_documents
from .tools import query_database_logic


async def handle_gradio_chat(message: str, history: List[Any], user_id: str) -> str:
    """Verarbeitet Nachrichten im Gradio-Chat und validiert die User-ID."""
    _ = history  # ChatInterface liefert den bisherigen Verlauf; wir brauchen ihn hier nicht.
    uid = (user_id or "").strip()
    if not uid:
        return "Bitte gib eine User-ID an (z.B. 'demo-user')."
    try:
        return await run_agent_turn(uid, message)
    except Exception as exc:  # noqa: BLE001 - wir zeigen Fehler direkt im UI
        return f"Fehler beim Agentenaufruf: {exc}"


async def handle_seed_wissensbasis() -> str:
    """Startet das Seeding der Beispiel-Dokumente."""
    try:
        result = await seed_example_documents()
        return f"{result.inserted} Beispiel-Dokumente gespeichert."
    except Exception as exc:  # noqa: BLE001
        return f"Seed fehlgeschlagen: {exc}"


def handle_db_preview(query_text: str) -> str:
    """Führt eine semantische Suche durch und zeigt die Ergebnisse."""
    question = (query_text or "").strip()
    if not question:
        return "Bitte gib eine Suchanfrage ein."
    return query_database_logic(question, n_results=4)


def handle_clear_history_ui(user_id: str) -> Tuple[List[Any], str]:
    """Leert die UI und entfernt die Historie für die User-ID."""
    feedback = clear_conversation(user_id)
    return [], feedback


def create_gradio_blocks() -> gr.Blocks:
    """Erzeugt die komplette Gradio-Oberfläche."""
    with gr.Blocks(title="RAG Agent Playground") as rag_ui:
        gr.Markdown("## RAG Agent Playground\nTeste den FastAPI-Agenten direkt im Browser.")

        with gr.Row():
            user_id_input = gr.Textbox(
                label="User-ID",
                value="demo-user",
                info="Eigene IDs erzeugen getrennte Gesprächshistorien.",
            )
            extra_clear_btn = gr.Button("Konversation leeren", variant="secondary")

        clear_feedback = gr.Markdown(value="")

        with gr.Accordion("Wissensbasis verwalten", open=True):
            # Zwei Helfer-Schritte: Seed + Direkt-Suche.
            seed_btn = gr.Button("Beispielwissen laden")
            seed_result = gr.Markdown(value="")
            seed_btn.click(fn=handle_seed_wissensbasis, outputs=seed_result)

            query_input = gr.Textbox(
                label="Semantische Vorschau",
                placeholder="Frag die Wissensbasis direkt …",
            )
            query_btn = gr.Button("Suche starten")
            query_result = gr.Markdown(value="")
            query_btn.click(fn=handle_db_preview, inputs=query_input, outputs=query_result)

        chat_ui = gr.ChatInterface(
            fn=handle_gradio_chat,
            additional_inputs=[user_id_input],
            type="messages",
            title="Chat mit dem Agenten",
            description=(
                "Stelle Fragen – der Agent nutzt zuerst Chroma und greift bei Bedarf aufs Web-Tool zurück."
            ),
        )

        extra_clear_btn.click(
            fn=handle_clear_history_ui,
            inputs=user_id_input,
            outputs=[chat_ui.chatbot, clear_feedback],
            queue=False,
        )

    # Queue verhindert, dass parallele Requests sich gegenseitig blockieren.
    return rag_ui.queue(default_concurrency_limit=2)

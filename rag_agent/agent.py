"""Konfiguration des Responses-Agenten und Hilfsfunktionen für Gespräche."""

from __future__ import annotations

from typing import Dict, List

from openai import AsyncOpenAI

from agents import Agent, Runner
from agents.items import ItemHelpers, TResponseInputItem
from agents.models.openai_responses import OpenAIResponsesModel

from .settings import OPENAI_API_KEY
from .tools import query_database, web_fetch_and_store


# ResponsesModel kapselt die OpenAI Responses API für strukturierte Agentenläufe.
responses_model = OpenAIResponsesModel(
    model="gpt-5-nano",
    openai_client=AsyncOpenAI(api_key=OPENAI_API_KEY),
)

# Der eigentliche Recherche-Agent inklusive Tool-Anbindung und Anweisungstext.
recherche_agent = Agent(
    name="Recherche-Agent",
    instructions=(
        "Du bist ein hilfreicher Assistent in einem RAG-System.\n"
        "Vorgehen:\n"
        "1) Nutze zuerst 'query_database' mit der Nutzerfrage.\n"
        "2) Wenn keine nützlichen Treffer vorhanden sind, rufe 'web_fetch_and_store' mit einer eindeutigen URL auf,\n"
        "   und frage danach erneut die Wissensbasis ab.\n"
        "3) Formuliere immer eine klare, vollständige End-Antwort und nenne relevante Quellen (Metadaten 'source')."
    ),
    model=responses_model,
    tools=[query_database, web_fetch_and_store],
)

# Einfache, in-memory gespeicherte Chat-Historien pro Nutzer-ID (für Demozwecke ausreichend).
conversation_histories: Dict[str, List[TResponseInputItem]] = {}


async def run_agent_turn(user_id: str, message: str) -> str:
    """Führt den Agentenlauf mit fortgeführter Historie aus."""
    previous_items = conversation_histories.get(user_id)
    # Wir bauen die Eingabe-Liste der Responses-API neu auf (alte Historie + aktuelle Frage).
    input_items: List[TResponseInputItem] = (
        ItemHelpers.input_to_new_input_list(previous_items)
        if previous_items is not None
        else []
    )
    input_items.extend(ItemHelpers.input_to_new_input_list(message))

    result = await Runner.run(recherche_agent, input_items)
    # Für die nächste Runde speichern wir die aktualisierte Historie als Input-Liste.
    conversation_histories[user_id] = result.to_input_list()
    return result.final_output


def clear_conversation(user_id: str) -> str:
    """Entfernt die gespeicherte Historie für eine User-ID."""
    uid = (user_id or "").strip()
    if not uid:
        return "Keine User-ID angegeben – nichts zu löschen."
    conversation_histories.pop(uid, None)
    return f"Konversation für '{uid}' gelöscht."

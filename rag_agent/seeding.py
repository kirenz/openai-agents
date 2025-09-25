"""Hilfsfunktionen zum Befüllen der Wissensbasis mit Beispieldaten."""

from __future__ import annotations

from .schemas import SeedResult
from .vector_store import add_documents


async def seed_example_documents() -> SeedResult:
    """Speichert Demo-Datensätze in Chroma für schnelle Tests."""
    # Mini-Dataset, damit Studierende ohne eigenen Crawl sofort testen können.
    docs = [
        # Mitarbeiter-Profile
        "Mitarbeiterprofil: Name: Anna Schneider. Rolle: Data Analystin. Team: Marketing Analytics. "
        "Skills: SQL, Python (Pandas, Altair), dbt. Projekte: Kampagnen-Dashboard, Churn-Analyse. "
        "Standort: Stuttgart. Verfügbarkeit: 80%. Ansprechpartner: lead.marketing.analytics@example.com",
        "Mitarbeiterprofil: Name: Mehmet Yilmaz. Rolle: ML Engineer. Team: AI Platform. "
        "Skills: LangGraph, Agents SDK (OpenAI), ChromaDB, Kubernetes, CI/CD. "
        "Projekte: RAG-Bot für Service, Event-Streaming-Ingestion. Standort: Remote (DE). Verfügbarkeit: 60%.",
        "Mitarbeiterprofil: Name: Julia Roth. Rolle: Product Owner Conversational AI. Team: Digital Services. "
        "Skills: Cognigy, Voiceflow, Evaluationsframeworks, GDPR-Assessments. "
        "Projekte: Support-Assistant v2, NLU-Intents Katalog. Standort: München. Verfügbarkeit: 100%.",
        # Policy
        "Policy: Datenklassifizierung. Öffentlich, Intern, Vertraulich, Streng Vertraulich. "
        "Streng Vertraulich: Keine Nutzung in externen KI-Diensten. "
        "Vertraulich: Nutzung nur mit freigegebenen Providern und aktiviertem Audit-Logging. "
        "Intern: Nutzung in Experimenten erlaubt, aber keine personenbezogenen Daten.",
        # FAQ
        "FAQ: Wie wähle ich ein Framework für einen KI-Agenten? "
        "Für schnelle Prototypen: Agents SDK (OpenAI) + ChromaDB. "
        "Für komplexe Orchestrierung: LangGraph. "
        "Für Voice/Contact-Center: Cognigy. "
        "Für No-Code-Automationsketten: n8n (mit generativen Nodes).",
    ]
    metas = [
        {"entity": "Anna Schneider", "type": "user_profile"},
        {"entity": "Mehmet Yilmaz", "type": "user_profile"},
        {"entity": "Julia Roth", "type": "user_profile"},
        {"entity": "Policy Team", "type": "policy"},
        {"entity": "AI Practices", "type": "faq"},
    ]
    add_documents(docs, metas)
    return SeedResult(inserted=len(docs))

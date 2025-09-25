"""Pydantic-Modelle für die FastAPI-Endpunkte."""

from __future__ import annotations

from pydantic import BaseModel


class ChatRequest(BaseModel):
    user_id: str
    message: str


class SeedResult(BaseModel):
    inserted: int

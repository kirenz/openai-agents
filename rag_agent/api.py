"""FastAPI-Router mit den HTTP-Endpunkten."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .agent import run_agent_turn
from .schemas import ChatRequest, SeedResult
from .seeding import seed_example_documents

# Router wird im Application-Fabrik eingebunden und stellt HTTP-Endpunkte bereit.
router = APIRouter()


@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    try:
        final_output = await run_agent_turn(request.user_id, request.message)
        return {"user_id": request.user_id, "response": final_output}
    except Exception as exc:  # noqa: BLE001 - dem Client strukturiert melden
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/seed_example_users", response_model=SeedResult)
async def seed_example_users():
    try:
        return await seed_example_documents()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc

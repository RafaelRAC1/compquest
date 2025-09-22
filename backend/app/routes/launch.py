from fastapi import APIRouter, HTTPException
from app.utils.Player import Player
from app.utils.pick_questions import pick_questions
from app.utils.session_manager import session_manager
from app.utils.websocket_manager import websocket_manager
from app.utils.game_logic import game_logic
import random
import asyncio

router = APIRouter(prefix="/compquest")

@router.post("/launch")
async def create_session(player: Player):
    questions = pick_questions()
    session_id = session_manager.create_session(player.name, questions)
    return {"session_id": session_id, "message": "Session created, waiting for second player."}

@router.post("/join-session/{session_id}")
async def join_session(session_id: str, player: Player):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if len(session["players"]) >= 2:
        raise HTTPException(status_code=400, detail="Session is full")
    if player.name in session["players"]:
        raise HTTPException(status_code=400, detail="Player already in session")

    success = session_manager.add_player_to_session(session_id, player.name)
    if not success:
        raise HTTPException(status_code=400, detail="Could not join session")

    if len(session["players"]) == 2:
        await _notify_session_ready(session_id)
        return {"session_id": session_id, "message": "Game ready!", "players": session["players"]}
    else:
        return {"session_id": session_id, "message": "Waiting for second player...", "players": session["players"]}

@router.post("/join-random-session")
async def join_random_session(player: Player):
    available_sessions = session_manager.get_available_sessions()
    if not available_sessions:
        raise HTTPException(status_code=404, detail="No available sessions found")
    
    session_id, session = random.choice(available_sessions)

    if player.name in session["players"]:
        raise HTTPException(status_code=400, detail="Player already in session")

    success = session_manager.add_player_to_session(session_id, player.name)
    if not success:
        raise HTTPException(status_code=400, detail="Could not join session")

    if len(session["players"]) == 2:
        await _notify_session_ready(session_id)
        return {"session_id": session_id, "message": "Game ready!", "players": session["players"]}
    else:
        return {"session_id": session_id, "message": "Waiting for second player...", "players": session["players"]}

@router.get("/session/{session_id}")
def get_session(session_id: str):
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/sessions")
def get_all_sessions():
    return {
        "total_sessions": len(session_manager.sessions),
        "waiting_sessions": len([s for s in session_manager.sessions.values() if s["status"] == "waiting"]),
        "active_sessions": len([s for s in session_manager.sessions.values() if s["status"] == "ready"]),
        "sessions": {sid: {"players": s["players"], "status": s["status"]} for sid, s in session_manager.sessions.items()}
    }

async def _notify_session_ready(session_id: str):
    print(f"Notifying session ready: {session_id}")
    session = session_manager.get_session(session_id)
    
    session_data = session.copy()
    session_data["players_ready"] = list(session.get("players_ready", set()))
    
    await websocket_manager.broadcast_to_session(session_id, {
        "event": "session_ready",
        "session": session_data
    })
    
    await asyncio.sleep(2)
    await game_logic.send_question(session_id)
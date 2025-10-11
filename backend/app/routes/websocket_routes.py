from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.session_manager import session_manager
from app.utils.game_logic import game_logic
import asyncio

router = APIRouter(prefix="/compquest")

@router.websocket("/ws/{session_id}/{player_name}")
async def websocket_game(websocket: WebSocket, session_id: str, player_name: str):
    await websocket.accept()
    print(f"WebSocket connected: {player_name} in session {session_id}")
    
    session_manager.add_connection(session_id, player_name, websocket)

    session = session_manager.get_session(session_id)
    if not session:
        await websocket.send_json({"event": "error", "message": "Session not found"})
        return

    print(f"Session status: {session['status']}, players: {session['players']}")

    if session["status"] == "ready":
        session_data = session.copy()
        session_data["players_ready"] = list(session.get("players_ready", set()))
        
        await websocket.send_json({
            "event": "session_ready",
            "session": session_data
        })
        
        if session["current_index"] == 0 and not session.get("round_answered", False):
            await asyncio.sleep(1)
            await game_logic.send_question(session_id)

    try:
        while True:
            data = await websocket.receive_json()
            if data["event"] == "answer":
                await game_logic.handle_answer(session_id, player_name, data["answer"])
            elif data["event"] == "ready_next":
                await game_logic.handle_ready_next(session_id, player_name)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {player_name}")
        session_manager.remove_connection(session_id, player_name)
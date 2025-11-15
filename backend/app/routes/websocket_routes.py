from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.session_manager import session_manager
from app.utils.game_logic import game_logic
from app.utils.auth import verify_websocket_token
from app.utils.websocket_manager import websocket_manager
import asyncio

router = APIRouter(prefix="/compquest")

@router.websocket("/ws/{session_id}/{player_name}")
async def websocket_game(websocket: WebSocket, session_id: str, player_name: str):
    await websocket.accept()
    
    # Verifica token de autenticação
    if not await verify_websocket_token(websocket):
        await websocket.send_json({"error": "Token inválido ou ausente"})
        await websocket.close(code=1008)
        return
    print(f"WebSocket conectado: {player_name} na sessão {session_id}")
    
    session_manager.add_connection(session_id, player_name, websocket)

    session = session_manager.get_session(session_id)
    if not session:
        await websocket.send_json({"event": "error", "message": "Sessão não encontrada"})
        return

    print(f"Status da sessão: {session['status']}, jogadores: {session['players']}")

    if session["status"] == "ready":
        session_data = session.copy()
        session_data["players_ready"] = list(session.get("players_ready", set()))
        session_data["has_used_turing"] = session.get("has_used_turing", {})
        session_data["has_used_memory_stick"] = session.get("has_used_memory_stick", {})
        
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
            elif data["event"] == "use_turing":
                await game_logic.handle_use_turing(session_id, player_name)
            elif data["event"] == "use_memory_stick":
                await game_logic.handle_use_memory_stick(session_id, player_name)
    except WebSocketDisconnect:
        print(f"WebSocket desconectado: {player_name}")
        session_manager.remove_connection(session_id, player_name)
        
        # Notifica os jogadores restantes que este jogador desconectou
        session = session_manager.get_session(session_id)
        if session:
            # Obtém os jogadores restantes (aqueles ainda conectados)
            remaining_connections = session_manager.get_connections(session_id)
            remaining_players = list(remaining_connections.keys())
            
            # Notifica os jogadores restantes
            if remaining_players:
                await websocket_manager.broadcast_to_session(session_id, {
                    "event": "player_disconnected",
                    "disconnected_player": player_name,
                    "message": f"{player_name} saiu da partida"
                })
from typing import Dict
from fastapi import WebSocket
import uuid

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, dict] = {}
        self.connections: Dict[str, Dict[str, WebSocket]] = {}
    
    def create_session(self, player_name: str, questions: list) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "players": [player_name],
            "status": "waiting",
            "questions": questions,
            "current_index": 0,
            "scores": {player_name: 0},
            "streaks": {player_name: 0},
            "has_used_turing": {player_name: False},
            "has_used_memory_stick": {player_name: False},
            "round_answered": False,
            "round_winner": None,
            "round_answer": None,
            "round_start_time": None,
            "players_ready": set()
        }
        return session_id
    
    def add_player_to_session(self, session_id: str, player_name: str) -> bool:
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        if len(session["players"]) >= 2 or player_name in session["players"]:
            return False
        
        session["players"].append(player_name)
        session["scores"][player_name] = 0
        session["streaks"][player_name] = 0
        session["has_used_turing"][player_name] = False
        session["has_used_memory_stick"][player_name] = False
        
        if len(session["players"]) == 2:
            session["status"] = "ready"
        
        return True
    
    def get_session(self, session_id: str) -> dict:
        return self.sessions.get(session_id)
    
    def add_connection(self, session_id: str, player_name: str, websocket: WebSocket):
        if session_id not in self.connections:
            self.connections[session_id] = {}
        self.connections[session_id][player_name] = websocket
    
    def remove_connection(self, session_id: str, player_name: str):
        if session_id in self.connections and player_name in self.connections[session_id]:
            del self.connections[session_id][player_name]
    
    def get_connections(self, session_id: str) -> Dict[str, WebSocket]:
        return self.connections.get(session_id, {})
    
    def get_available_sessions(self) -> list:
        return [(sid, s) for sid, s in self.sessions.items() if s["status"] == "waiting"]

session_manager = SessionManager()
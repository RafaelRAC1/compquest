from .session_manager import session_manager

class WebSocketManager:
    async def broadcast_to_session(self, session_id: str, message: dict):
        connections = session_manager.get_connections(session_id)
        for player_name, ws in connections.items():
            try:
                await ws.send_json(message)
                print(f"Message sent to {player_name}")
            except Exception as e:
                print(f"Error sending to {player_name}: {e}")
    
    async def send_to_player(self, session_id: str, player_name: str, message: dict):
        connections = session_manager.get_connections(session_id)
        if player_name in connections:
            try:
                await connections[player_name].send_json(message)
            except Exception as e:
                print(f"Error sending to {player_name}: {e}")

websocket_manager = WebSocketManager()
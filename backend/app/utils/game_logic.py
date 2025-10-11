from .session_manager import session_manager
from .websocket_manager import websocket_manager
from ..database import db_manager
import time
import asyncio

class GameLogic:
    async def send_question(self, session_id: str):
        session = session_manager.get_session(session_id)
        if not session:
            return
            
        idx = session["current_index"]
        
        if idx >= len(session["questions"]):
            return
            
        question = session["questions"][idx].copy()
        question_to_send = {
            "question": question["question"],
            "options": question["options"],
            "oracle_hint": question.get("oracle_hint", "")
        }

        session["round_answered"] = False
        session["round_winner"] = None
        session["round_answer"] = None
        session["round_start_time"] = time.time()
        session["players_ready"] = set()

        print(f"Sending question {idx + 1} for session {session_id}")
        print(f"Question: {question['question']}")
        print(f"Options: {question['options']}")
        print(f"Correct answer: '{question['answer']}'")

        message = {
            "event": "new_question",
            "index": idx + 1,
            "total": len(session["questions"]),
            "question": question_to_send
        }
        
        await websocket_manager.broadcast_to_session(session_id, message)
    
    async def handle_answer(self, session_id: str, player_name: str, answer: str):
        session = session_manager.get_session(session_id)
        if not session:
            return
        
        if session.get("round_answered", False):
            print(f"Late answer ignored from {player_name}")
            return
        
        print(f"{player_name} answered: {answer}")
        
        session["round_answered"] = True
        session["round_winner"] = player_name
        session["round_answer"] = answer
        session["round_time"] = time.time() - session["round_start_time"]
        
        idx = session["current_index"]
        current_question = session["questions"][idx]
        correct_answer = current_question["answer"]
        
        answer_options = current_question["options"]
        answer_index = ord(answer.upper()) - ord('A')
        
        if 0 <= answer_index < len(answer_options):
            selected_answer_text = answer_options[answer_index]
            is_correct = selected_answer_text == correct_answer
        else:
            selected_answer_text = answer
            is_correct = False
        
        if is_correct:
            points = self._calculate_points(idx)
            session["scores"][player_name] += points
        
        await websocket_manager.broadcast_to_session(session_id, {
            "event": "player_answered",
            "player": player_name,
            "response_time": round(session["round_time"], 2)
        })
        
        await asyncio.sleep(1.5)
        
        await websocket_manager.broadcast_to_session(session_id, {
            "event": "round_result",
            "winner": player_name,
            "answer": selected_answer_text,
            "answer_letter": answer,
            "correct_answer": correct_answer,
            "correct": is_correct,
            "response_time": round(session["round_time"], 2),
            "scores": session["scores"],
            "explanation": current_question.get("explanation", "")
        })
    
    def _calculate_points(self, question_index: int) -> int:
        match question_index:
            case 0 | 1 | 2 | 3:
                return 100
            case 4 | 5 | 6 | 7:
                return 200
            case 8 | 9:
                return 400
            case _:
                return 0
    
    async def handle_ready_next(self, session_id: str, player_name: str):
        session = session_manager.get_session(session_id)
        if not session:
            return
            
        session["players_ready"].add(player_name)
        
        print(f"{player_name} ready for next question. Total ready: {len(session['players_ready'])}")
        
        await websocket_manager.broadcast_to_session(session_id, {
            "event": "player_ready",
            "player": player_name,
            "total_ready": len(session["players_ready"])
        })
        
        if len(session["players_ready"]) >= len(session["players"]):
            await websocket_manager.broadcast_to_session(session_id, {
                "event": "both_ready"
            })
            
            await asyncio.sleep(2)
            
            session["current_index"] += 1
            
            if session["current_index"] < len(session["questions"]):
                await self.send_question(session_id)
            else:
                await self._handle_game_over(session_id)
    
    async def _handle_game_over(self, session_id: str):
        session = session_manager.get_session(session_id)
        final_scores = session["scores"]
        max_score = max(final_scores.values()) if final_scores.values() else 0
        winners = [p for p, s in final_scores.items() if s == max_score]
        
        await self._save_game_results(session_id, final_scores, winners)
        
        await websocket_manager.broadcast_to_session(session_id, {
            "event": "game_over",
            "final_scores": final_scores,
            "winners": winners,
            "is_tie": len(winners) > 1
        })
    
    async def _save_game_results(self, session_id: str, final_scores: dict, winners: list):
        """Save game results to database"""
        try:
            match_id = db_manager.create_match()
            
            question_ids = []
            if "questions" in session_manager.get_session(session_id):
                question_ids = [q.get("id") for q in session_manager.get_session(session_id)["questions"] if q.get("id")]
            
            if question_ids:
                db_manager.add_questions_to_match(match_id, question_ids)
            
            for player_name, score in final_scores.items():
                player_id = db_manager.get_or_create_player(player_name)
                won = player_name in winners
                db_manager.save_match_result(match_id, player_id, score, won)
            
            print(f"Game results saved to database for match {match_id}")
            
        except Exception as e:
            print(f"Error saving game results: {e}")

game_logic = GameLogic()
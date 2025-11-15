from .session_manager import session_manager
from .websocket_manager import websocket_manager
from ..database import db_manager
import time
import asyncio
import random

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

        print(f"Enviando questão {idx + 1} para sessão {session_id}")
        print(f"Questão: {question['question']}")
        print(f"Opções: {question['options']}")
        print(f"Resposta correta: '{question['answer']}'")

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
            print(f"Resposta tardia ignorada de {player_name}")
            return
        
        print(f"{player_name} respondeu: {answer}")
        
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
        
        # Calcula pontos base para esta questão
        base_points = self._calculate_points(idx)
        
        if is_correct:
            # RESPOSTA CORRETA: Aplica sistema de multiplicador de sequência
            # Obtém sequência atual e calcula multiplicador
            current_streak = session["streaks"].get(player_name, 0)
            multiplier = self._calculate_multiplier(current_streak)
            
            # Aplica multiplicador aos pontos base e adiciona à pontuação do jogador
            points = int(base_points * multiplier)
            session["scores"][player_name] += points
            
            # Aumenta sequência em +1
            session["streaks"][player_name] = current_streak + 1
        else:
            # RESPOSTA INCORRETA: Aplica sistema de penalidade por erro
            # Penalidade: 20% dos pontos base são concedidos ao oponente
            # O jogador que respondeu incorretamente não perde pontos
            # A sequência do jogador é resetada para 0
            penalty = int(base_points * 0.2)
            
            # Encontra o oponente e concede os pontos de penalidade
            opponent_name = [p for p in session["players"] if p != player_name][0]
            session["scores"][opponent_name] += penalty
            
            # Reseta sequência para 0 por resposta errada
            session["streaks"][player_name] = 0
        
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
            "streaks": session["streaks"],
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
    
    def _calculate_multiplier(self, streak: int) -> float:
        """Calcula multiplicador de pontuação baseado na sequência
        O parâmetro streak é a sequência atual antes de responder esta questão.
        O multiplicador é aplicado à próxima resposta correta:
        - 1 resposta correta: x1.0
        - 2 respostas corretas: x1.1
        - 3 respostas corretas: x1.2
        - ...
        - 10+ respostas corretas: x2.0
        """
        if streak >= 9:  # Para a 10ª resposta correta e além
            return 2.0
        else:
            return 1.0 + streak * 0.1
    
    async def handle_use_turing(self, session_id: str, player_name: str):
        """Lida com a ativação do poder especial Alan Turing"""
        session = session_manager.get_session(session_id)
        if not session:
            return
        
        # Verifica se o jogador já usou o poder
        if session["has_used_turing"].get(player_name, False):
            print(f"{player_name} tentou usar Alan Turing mas já o usou")
            return
        
        # Verifica se a rodada já foi respondida
        if session.get("round_answered", False):
            print(f"Uso tardio de Alan Turing ignorado de {player_name}")
            return
        
        print(f"{player_name} usou o poder Alan Turing")
        
        # Marca como usado
        session["has_used_turing"][player_name] = True
        
        # Obtém a questão atual
        idx = session["current_index"]
        current_question = session["questions"][idx]
        correct_answer = current_question["answer"]
        
        # Encontra a letra da resposta correta
        answer_options = current_question["options"]
        answer_letter = None
        for i, option in enumerate(answer_options):
            if option == correct_answer:
                answer_letter = chr(ord('A') + i)
                break
        
        if answer_letter is None:
            print(f"Erro: Não foi possível encontrar a letra da resposta correta para a questão {idx}")
            return
        
        # Marca a rodada como respondida
        session["round_answered"] = True
        session["round_winner"] = player_name
        session["round_answer"] = answer_letter
        session["round_time"] = time.time() - session["round_start_time"]
        
        # Calcula pontos base (Alan Turing usa multiplicador x1.0, ignorando sequência)
        base_points = self._calculate_points(idx)
        points = int(base_points * 1.0)  # Sempre multiplicador x1.0
        
        # Concede pontos
        session["scores"][player_name] += points
        
        # Reseta sequência para 0 (Alan Turing reseta a sequência)
        session["streaks"][player_name] = 0
        
        # Transmite que o jogador usou Alan Turing
        await websocket_manager.broadcast_to_session(session_id, {
            "event": "player_answered",
            "player": player_name,
            "response_time": round(session["round_time"], 2),
            "used_turing": True
        })
        
        await asyncio.sleep(1.5)
        
        # Transmite resultado da rodada
        await websocket_manager.broadcast_to_session(session_id, {
            "event": "round_result",
            "winner": player_name,
            "answer": correct_answer,
            "answer_letter": answer_letter,
            "correct_answer": correct_answer,
            "correct": True,
            "response_time": round(session["round_time"], 2),
            "scores": session["scores"],
            "streaks": session["streaks"],
            "explanation": current_question.get("explanation", ""),
            "used_turing": True
        })
    
    async def handle_use_memory_stick(self, session_id: str, player_name: str):
        """Lida com a ativação do poder especial Pente de Memória (Memory Stick)"""
        session = session_manager.get_session(session_id)
        if not session:
            return
        
        # Verifica se o jogador já usou o poder
        if session["has_used_memory_stick"].get(player_name, False):
            print(f"{player_name} tentou usar Pente de Memória mas já o usou")
            return
        
        # Verifica se a rodada já foi respondida
        if session.get("round_answered", False):
            print(f"Uso tardio de Pente de Memória ignorado de {player_name}")
            return
        
        print(f"{player_name} usou Pente de Memória (Memory Stick)")
        
        # Marca como usado
        session["has_used_memory_stick"][player_name] = True
        
        # Obtém a questão atual para determinar a dificuldade
        idx = session["current_index"]
        current_question = session["questions"][idx]
        
        # Determina dificuldade baseada no índice da questão
        if idx < 4:
            difficulty = "facil"
        elif idx < 8:
            difficulty = "medio"
        else:
            difficulty = "dificil"
        
        # Obtém todas as questões da mesma dificuldade do banco de dados
        all_questions = db_manager.get_questions_by_difficulty(difficulty)
        
        # Obtém IDs das questões já usadas nesta sessão
        used_question_ids = {q.get("id") for q in session["questions"] if q.get("id")}
        
        # Filtra questões que já foram usadas
        available_questions = [q for q in all_questions if q.get("id") not in used_question_ids]
        
        if not available_questions:
            print(f"Nenhuma questão disponível de dificuldade {difficulty} para substituir")
            # Se não houver substituição disponível, não substitui
            await websocket_manager.broadcast_to_session(session_id, {
                "event": "memory_stick_failed",
                "message": "Não há questões disponíveis para substituir"
            })
            return
        
        # Escolhe uma questão aleatória das disponíveis
        replacement_question = random.choice(available_questions)
        
        # Converte para o mesmo formato das questões da sessão
        correct_answer = None
        options = []
        
        for option in replacement_question['options']:
            options.append(option['text'])
            if option['correct']:
                correct_answer = option['text']
        
        question_data = {
            "question": replacement_question['question'],
            "options": options,
            "answer": correct_answer,
            "oracle_hint": replacement_question['hint'],
            "explanation": replacement_question['explanation'],
            "id": replacement_question['id']
        }
        
        # Substitui a questão atual
        session["questions"][idx] = question_data
        
        # Reseta o estado da rodada
        session["round_answered"] = False
        session["round_winner"] = None
        session["round_answer"] = None
        session["round_start_time"] = time.time()
        session["players_ready"] = set()
        
        # Transmite nova questão
        question_to_send = {
            "question": question_data["question"],
            "options": question_data["options"],
            "oracle_hint": question_data.get("oracle_hint", "")
        }
        
        await websocket_manager.broadcast_to_session(session_id, {
            "event": "memory_stick_used",
            "player": player_name,
            "message": "💾 Pente de Memória ativado! Carregando uma nova questão..."
        })
        
        await asyncio.sleep(1)
        
        await websocket_manager.broadcast_to_session(session_id, {
            "event": "new_question",
            "index": idx + 1,
            "total": len(session["questions"]),
            "question": question_to_send,
            "memory_stick_used": True
        })
    
    async def handle_ready_next(self, session_id: str, player_name: str):
        session = session_manager.get_session(session_id)
        if not session:
            return
            
        session["players_ready"].add(player_name)
        
        print(f"{player_name} pronto para próxima questão. Total pronto: {len(session['players_ready'])}")
        
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
            "final_streaks": session["streaks"],
            "winners": winners,
            "is_tie": len(winners) > 1
        })
    
    async def _save_game_results(self, session_id: str, final_scores: dict, winners: list):
        """Salva resultados do jogo no banco de dados"""
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
            
            print(f"Resultados do jogo salvos no banco de dados para partida {match_id}")
            
        except Exception as e:
            print(f"Erro ao salvar resultados do jogo: {e}")

game_logic = GameLogic()
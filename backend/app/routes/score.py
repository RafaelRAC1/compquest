from fastapi import status, HTTPException
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from ..database import db_manager
from app.utils.auth import verify_token

router = APIRouter(prefix="/compquest")

class ScoreRequest(BaseModel):
    player_name: str
    score: int
    won: bool = False

class ScoreResponse(BaseModel):
    player_name: str
    score: int
    won: bool
    match_id: int
    date: str

class PlayerStatsResponse(BaseModel):
    player_name: str
    total_matches: int
    total_score: int
    avg_score: float
    wins: int
    best_score: int

@router.post("/score")
async def save_score(score_request: ScoreRequest, token: bool = Depends(verify_token)):
    try:
        player_id = db_manager.get_or_create_player(score_request.player_name)
        
        match_id = db_manager.create_match()
        
        db_manager.save_match_result(
            match_id=match_id,
            player_id=player_id,
            score=score_request.score,
            won=score_request.won
        )
        
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT data FROM partida WHERE id = ?", (match_id,))
            result = cursor.fetchone()
            match_date = result['data'] if result else None
        
        return ScoreResponse(
            player_name=score_request.player_name,
            score=score_request.score,
            won=score_request.won,
            match_id=match_id,
            date=match_date
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving score: {str(e)}")

@router.get("/score/{player_name}")
async def get_player_stats(player_name: str, token: bool = Depends(verify_token)):
    try:
        stats = db_manager.get_player_stats(player_name)
        return PlayerStatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting player stats: {str(e)}")

@router.get("/score")
async def get_all_scores(token: bool = Depends(verify_token)):
    try:
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT j.nome, j.score, j.venceu, p.data, p.id as match_id
                FROM joga j
                JOIN jogador jg ON j.id_jogador = jg.id
                JOIN partida p ON j.id_partida = p.id
                ORDER BY p.data DESC
                LIMIT 50
            """)
            
            scores = []
            for row in cursor.fetchall():
                scores.append({
                    "player_name": row['nome'],
                    "score": row['score'],
                    "won": bool(row['venceu']),
                    "date": row['data'],
                    "match_id": row['match_id']
                })
            
            return {"scores": scores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting scores: {str(e)}")

@router.get("/top-players")
async def get_top_players(limit: int = 3, token: bool = Depends(verify_token)):
    try:
        top_players = db_manager.get_top_players(limit)
        return {"top_players": top_players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting top players: {str(e)}")
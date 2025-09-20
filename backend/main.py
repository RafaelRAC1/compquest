from fastapi import FastAPI, status, HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from app.utils.Player import Player
import uuid

app = FastAPI()
router = APIRouter(prefix="/compquest")

@router.get("/health", status_code=status.HTTP_200_OK)
async def root():
    return JSONResponse(
        status_code=200,
        content={"message": "OK"}
    )
    
@router.get("/launch", status_code=status.HTTP_200_OK)
async def root():
    return JSONResponse(
        status_code=200,
        content={"message": "OK"}
    )
    
sessions = {}

@router.post("/create-session")
def create_session(player: Player):
    session_id = str(uuid.uuid4())
    sessions[session_id] = {
        "players": [player.name],
        "status": "waiting"  # can be "waiting" or "ready"
    }
    return {"session_id": session_id, "message": "Session created, waiting for second player."}

@router.post("/join-session/{session_id}")
def join_session(session_id: str, player: Player):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session = sessions[session_id]

    if len(session["players"]) >= 2:
        raise HTTPException(status_code=400, detail="Session is full")

    if player.name in session["players"]:
        raise HTTPException(status_code=400, detail="Player already in session")

    session["players"].append(player.name)

    if len(session["players"]) == 2:
        session["status"] = "ready"
        return {"session_id": session_id, "message": "Game ready!", "players": session["players"]}
    else:
        return {"session_id": session_id, "message": "Waiting for second player...", "players": session["players"]}

@router.get("/session/{session_id}")
def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return sessions[session_id]

app.include_router(router)
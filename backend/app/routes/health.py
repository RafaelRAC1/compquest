from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from app.utils.session_manager import session_manager

router = APIRouter(prefix="/compquest")

@router.get("/health", status_code=status.HTTP_200_OK,)
async def health_check():
    session_stats = {
        "total_sessions": len(session_manager.sessions),
        "waiting_sessions": len([s for s in session_manager.sessions.values() if s["status"] == "waiting"]),
        "open_sessions": len([s for s in session_manager.sessions.values() if s["status"] == "ready"]),
    }
    return JSONResponse(
        status_code=200,
        content={
            "status": "Running!",
            "sessions": session_stats
        }
    )
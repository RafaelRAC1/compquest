from fastapi import status
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/compquest")

@router.get("/score", status_code=status.HTTP_200_OK)
async def root():
    return JSONResponse(
        status_code=200,
        content={"player": "TBD", "score":"TBD", "date":"TBD"}
    )
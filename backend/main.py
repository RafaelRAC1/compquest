from fastapi import FastAPI, status
from fastapi import APIRouter
from fastapi.responses import JSONResponse

app = FastAPI()
router = APIRouter(prefix="/compquest")

@router.get("/health", status_code=status.HTTP_200_OK)
async def root():
    return JSONResponse(
        status_code=200,
        content={"message": "OK"}
    )

app.include_router(router)
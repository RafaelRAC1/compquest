from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import launch, websocket_routes, health, score
import uvicorn

app = FastAPI(title="CompQuest API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(score.router)
app.include_router(health.router)
app.include_router(launch.router)
app.include_router(websocket_routes.router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
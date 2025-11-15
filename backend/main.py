from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.routes import launch, websocket_routes, health, score
from app.database import db_manager
from app.migrate_questions import migrate_questions
import uvicorn

app = FastAPI(title="CompQuest API")

@app.on_event("startup")
async def startup_event():
    """Executa migração se o banco de dados estiver vazio"""
    if not db_manager.has_questions():
        print("Banco de dados está vazio. Executando migração para carregar questões do JSON...")
        try:
            migrate_questions()
            print("Migração concluída com sucesso!")
        except Exception as e:
            print(f"ERRO: Falha ao migrar questões: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Banco de dados já possui questões. Pulando migração.")

@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """
    Manipulador de exceções personalizado para formatar erros de autenticação conforme solicitado.
    """
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        # Verifica se o detail é um dict com a chave "error" (da autenticação)
        if isinstance(exc.detail, dict) and "error" in exc.detail:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"error": exc.detail["error"]}
            )
    # Para outras exceções HTTP, usa comportamento padrão
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

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
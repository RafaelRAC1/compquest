from fastapi import Header, HTTPException, status
from typing import Annotated

# Token de autenticação fixo
AUTH_TOKEN = "my_secret_token"

async def verify_token(authorization: Annotated[str | None, Header()] = None):
    """
    Verifica o token de autenticação do cabeçalho Authorization.
    Levanta HTTPException com 401 se o token estiver ausente ou inválido.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token inválido ou ausente"}
        )
    
    # Verifica se começa com "Bearer "
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token inválido ou ausente"}
        )
    
    # Extrai o token
    token = authorization[7:]  # Remove o prefixo "Bearer "
    
    # Valida o token
    if token != AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token inválido ou ausente"}
        )
    
    return True

async def verify_websocket_token(websocket) -> bool:
    """
    Verifica o token de autenticação do cabeçalho Authorization do WebSocket ou parâmetro de consulta.
    Retorna True se válido, False caso contrário.
    """
    # Tenta o cabeçalho primeiro
    authorization = websocket.headers.get("authorization") or websocket.headers.get("Authorization")
    
    if authorization:
        # Verifica se começa com "Bearer "
        if authorization.startswith("Bearer "):
            token = authorization[7:]  # Remove o prefixo "Bearer "
            return token == AUTH_TOKEN
    
    # Fallback para parâmetro de consulta (para conexões WebSocket do navegador)
    query_params = dict(websocket.query_params)
    token = query_params.get("token")
    
    if token:
        return token == AUTH_TOKEN
    
    return False


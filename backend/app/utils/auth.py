from fastapi import HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

# Token de autenticação fixo
AUTH_TOKEN = "my_secret_token"

# Configura o esquema de segurança Bearer para Swagger
# auto_error=False permite que tratemos o erro manualmente
security = HTTPBearer(auto_error=False)

async def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)):
    """
    Verifica o token de autenticação do cabeçalho Authorization.
    Levanta HTTPException com 401 se o token estiver ausente ou inválido.
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Token inválido ou ausente"}
        )
    
    # Extrai o token
    token = credentials.credentials
    
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


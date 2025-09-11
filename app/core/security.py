# /core/security.py

from datetime import datetime, timedelta, timezone
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt

# ATUALIZADO: Importando o objeto 'settings' para centralizar a configuração
from core.config import settings

# REMOVIDO: Variáveis hardcoded. Agora usamos o 'settings'.
# SECRET_KEY = "sua_chave_secreta_supersegura" 
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 60

# --- Hashing de Senha ---

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# MANTIDO: Sua função original, apenas renomeada para padronização.
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# MANTIDO: Sua função original.
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# --- Manipulação de Tokens JWT ---

# MANTIDO: Sua função original, com as devidas atualizações.
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    # ATUALIZADO: Usando timezone.utc para datas e horas, que é mais seguro.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire, "type": "access"})
    
    # ATUALIZADO: Usando as configurações importadas do settings.
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# MANTIDO: Sua função original, com as devidas atualizações.
def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    # ATUALIZADO: Usando timezone.utc e a variável de configuração que adicionamos.
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})

    # ATUALIZADO: Usando as configurações importadas do settings.
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

# MANTIDO: Sua função original para decodificar tokens, agora mais segura.
def decode_access_token(token: str):
    """
    Decodifica um token. Retorna o payload em caso de sucesso
    ou None em caso de erro (token expirado, inválido, etc).
    """
    try:
        # ATUALIZADO: Usando as configurações importadas do settings.
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str, expected_type: str = "access"):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != expected_type:
            return None  
        return payload
    except JWTError:
        return None


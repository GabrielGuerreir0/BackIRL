""" # /api/deps.py

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Dict

# Importações de configuração, sessão e modelos
from core.config import settings
from db.session import SessionLocal
from models.aluno import Aluno
from models.turma import Turma
from models.educador import Educador
from models.coordenador import Coordenador
from models.assistente_social import Assistente

# Importando a função utilitária de segurança
from core.security import decode_access_token

# --- 1. DEPENDÊNCIAS BÁSICAS ---

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

bearer_scheme = HTTPBearer()

def get_current_user_payload(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> Dict:
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if not payload or "id" not in payload or "role" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido, expirado ou mal formatado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


# --- 2. DEPENDÊNCIAS DE AUTORIZAÇÃO (REGRAS DE NEGÓCIO) ---

# Para o router de Alunos (e outros que precisem de permissão de Coordenador)
async def verificar_se_e_coordenador(payload: Dict = Depends(get_current_user_payload)):
    
    if payload.get("role") != "coordenador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas coordenadores podem realizar esta ação."
        )
    return payload

# Para o router de Frequência
async def verificar_permissao_para_modificar_frequencia(
    turma_id: int, 
    db: Session = Depends(get_db), 
    payload: Dict = Depends(get_current_user_payload)
):
    
    user_id, user_role = payload.get("id"), payload.get("role")
    if user_role in ["coordenador", "assistente_social"]:
        return payload
    if user_role == "educador":
        turma = db.query(Turma).filter(Turma.id == turma_id).first()
        if not turma:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Turma não encontrada")
        if turma.educador_id == user_id:
            return payload
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para modificar a frequência desta turma.")

async def verificar_permissao_para_ler_dados_turma(
    turma_id: int, 
    db: Session = Depends(get_db), 
    payload: Dict = Depends(get_current_user_payload)
):
    
    user_id, user_role = payload.get("id"), payload.get("role")
    if user_role in ["coordenador", "assistente_social"]:
        return payload
    if user_role == "educador":
        turma = db.query(Turma).filter(Turma.id == turma_id).first()
        if turma and turma.educador_id == user_id:
            return payload
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para visualizar os dados desta turma.")

async def verificar_permissao_para_ler_dados_aluno(
    aluno_id: int, 
    db: Session = Depends(get_db), 
    payload: Dict = Depends(get_current_user_payload)
):

    user_id, user_role = payload.get("id"), payload.get("role")
    if user_role in ["coordenador", "assistente_social"]:
        return payload
    if user_role == "educador":
        aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
        if not aluno or not aluno.turma_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aluno não encontrado ou não está matriculado.")
        if aluno.turma.educador_id == user_id:
            return payload
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para visualizar os dados deste aluno.")

async def verificar_se_e_educador_da_turma(
    turma_id: int, 
    db: Session = Depends(get_db), 
    payload: Dict = Depends(get_current_user_payload)
):
    user_id, user_role = payload.get("id"), payload.get("role")

    if user_role != "educador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Apenas educadores podem realizar esta ação."
        )

    turma = db.query(Turma).filter(Turma.id == turma_id).first()

    if not turma:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Turma não encontrada"
        )

    if turma.educador_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado. Você não é o educador responsável por esta turma."
        )
    
    return payload """
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.recuperacao_senha import (
    SolicitarRecuperacaoSchema,
    ValidarCodigoSchema,
    RedefinirSenhaSchema
)
from crud.recuperacao_senha import (
    iniciar_recuperacao_senha,
    validar_codigo,
    redefinir_senha
)

router = APIRouter(prefix="/api/v1/recuperacao", tags=["Recuperação de Senha"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/solicitar")
async def solicitar_recuperacao(
    dados: SolicitarRecuperacaoSchema,
    db: Session = Depends(get_db)
):
    """
    Solicita recuperação de senha.
    - Aceita qualquer email (educador, coordenador ou assistente social)
    - Envia um código de recuperação por email se o email existir
    """
    await iniciar_recuperacao_senha(db, dados.email)
    return {"mensagem": "Se o email existir, um código de recuperação será enviado"}

@router.post("/validar")
async def validar_codigo_recuperacao(
    dados: ValidarCodigoSchema,
    db: Session = Depends(get_db)
):
    """
    Valida o código de recuperação recebido por email.
    """
    validar_codigo(db, dados.email, dados.codigo)
    return {"mensagem": "Código válido"}

@router.post("/redefinir")
async def redefinir_senha_usuario(
    dados: RedefinirSenhaSchema,
    db: Session = Depends(get_db)
):
    """
    Redefine a senha após validar o código.
    """
    redefinir_senha(db, dados.email, dados.codigo, dados.nova_senha)
    return {"mensagem": "Senha redefinida com sucesso"}
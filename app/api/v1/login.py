from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import create_access_token, verify_password
from models.coordenador import Coordenador
from models.assistente_social import AssistenteSocial
from crud import educador as crud_educador
from schemas.login import LoginSchema

router = APIRouter()

@router.post("/login")
def login(
    form_data: LoginSchema, 
    db: Session = Depends(get_db)
):
    # 🔹 1. Tenta autenticar como Educador
    educador = crud_educador.autenticar_educador(db, form_data.email, form_data.password)
    if educador:
        role = "educador"
        access_token = create_access_token({"sub": educador.email, "role": role})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": role
        }

    # 🔹 2. Se não for educador, tenta como Coordenador
    user = db.query(Coordenador).filter(Coordenador.email == form_data.email).first()
    if user and verify_password(form_data.password, user.hashed_password):
        role = "coordenador"
        access_token = create_access_token({"sub": user.email, "role": role})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": role
        }

    user = db.query(AssistenteSocial).filter(AssistenteSocial.email == form_data.email).first()
    if user and verify_password(form_data.password, user.hashed_password):
        role = "assistente"
        access_token = create_access_token({"sub": user.email, "role": role})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": role
        }

    # 🔹 3. Se não encontrou em nenhum lugar, credenciais inválidas
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Email ou senha incorretos"
    )

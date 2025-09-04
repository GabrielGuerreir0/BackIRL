from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import create_access_token, verify_password
from api.v1.coordenador import crud_coordenador
from api.v1.educador import crud_educador
from api.v1.assistente_social import crud_assistente
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
    user = db.query(crud_coordenador.Coordenador).filter_by(email=form_data.email).first()
    if user and verify_password(form_data.password, user.hashed_password):
        role = "coordenador"
        access_token = create_access_token({"sub": user.email, "role": role})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": role
        }

    user = db.query(crud_assistente.Assistente).filter_by(email=form_data.email).first()
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

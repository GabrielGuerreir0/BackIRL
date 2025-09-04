from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.aluno import AlunoCreate, AlunoOut
from crud import aluno as crud_aluno
from typing import Optional, List
import shutil
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_access_token

router = APIRouter()

UPLOAD_DIR = "uploads/alunos/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Agora usando HTTPBearer em vez de OAuth2PasswordBearer
bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def coordenador_required(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials  # pega só o JWT do Authorization: Bearer <token>
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "coordenador":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Apenas coordenadores podem cadastrar alunos."
        )
    return payload

@router.post("/", response_model=AlunoOut)
def criar_aluno(
    nome: str = Form(...),
    data_nascimento: str = Form(...),
    sexo: str = Form(...),
    cpf: str = Form(...),
    naturalidade: str = Form(...),
    cor_raca: str = Form(...),
    endereco: str = Form(...),
    turma_id: int = Form(...),
    nome_responsavel: Optional[str] = Form(None),
    parentesco_responsavel: Optional[str] = Form(None),
    cpf_responsavel: Optional[str] = Form(None),
    telefone_responsavel: Optional[str] = Form(None),
    email_responsavel: Optional[str] = Form(None),
    necessidades_especiais: Optional[str] = Form(None),
    alergias: Optional[str] = Form(None),
    tipo_sanguineo: Optional[str] = Form(None),
    documento_crianca: Optional[UploadFile] = File(None),
    documento_responsavel: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    _: dict = Depends(coordenador_required)  # validação do token
):
    doc_crianca_path = None
    doc_responsavel_path = None

    if documento_crianca:
        doc_crianca_path = os.path.join(UPLOAD_DIR, documento_crianca.filename)
        with open(doc_crianca_path, "wb") as buffer:
            shutil.copyfileobj(documento_crianca.file, buffer)

    if documento_responsavel:
        doc_responsavel_path = os.path.join(UPLOAD_DIR, documento_responsavel.filename)
        with open(doc_responsavel_path, "wb") as buffer:
            shutil.copyfileobj(documento_responsavel.file, buffer)

    aluno_data = AlunoCreate(
        nome=nome,
        data_nascimento=data_nascimento,
        sexo=sexo,
        cpf=cpf,
        naturalidade=naturalidade,
        cor_raca=cor_raca,
        endereco=endereco,
        turma_id=turma_id,
        nome_responsavel=nome_responsavel,
        parentesco_responsavel=parentesco_responsavel,
        cpf_responsavel=cpf_responsavel,
        telefone_responsavel=telefone_responsavel,
        email_responsavel=email_responsavel,
        necessidades_especiais=necessidades_especiais,
        alergias=alergias,
        tipo_sanguineo=tipo_sanguineo,
        documento_crianca=doc_crianca_path,
        documento_responsavel=doc_responsavel_path
    )
    return crud_aluno.criar_aluno(db, aluno_data)

@router.get("/", response_model=List[AlunoOut])
def listar_alunos(db: Session = Depends(get_db), _: dict = Depends(coordenador_required)):
    return db.query(crud_aluno.Aluno).all()

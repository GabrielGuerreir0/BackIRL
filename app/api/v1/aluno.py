from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import shutil
import os
from fastapi.responses import FileResponse 

from db.session import SessionLocal
from schemas.aluno import AlunoCreate, AlunoUpdate, AlunoOut, DocumentoOut, DocumentoBase
from crud.aluno import (
    criar_aluno,
    get_aluno,
    get_alunos,
    atualizar_aluno,
    deletar_aluno,
    criar_documento,
    get_documento
)

from crud.turma import remover_aluno_da_turma
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_access_token
from models.aluno import Aluno, Documento

router = APIRouter()

# Define o diretório para salvar os uploads e o cria se não existir
UPLOAD_DIR = "uploads/alunos/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

bearer_scheme = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def coordenador_required(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "coordenador":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Apenas coordenadores podem realizar esta ação."
        )
    return payload

@router.post("/", response_model=AlunoOut, status_code=status.HTTP_201_CREATED)
def criar_aluno_route(
    aluno_data: AlunoCreate, 
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    
    db_aluno = criar_aluno(db=db, aluno=aluno_data)
    return db_aluno

@router.post("/{aluno_id}/documentos", response_model=DocumentoOut, status_code=status.HTTP_201_CREATED)
def upload_documento_route(
    aluno_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    db_aluno = get_aluno(db, aluno_id)
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    
    file_path = os.path.join(UPLOAD_DIR, f"{aluno_id}_{file.filename}")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao salvar o arquivo: {e}")
    
    documento_data = DocumentoBase(
        nome_arquivo=file.filename,
        caminho_arquivo=file_path
    )
    
    db_documento = criar_documento(db, aluno_id, documento_data)
    return db_documento

@router.get("/", response_model=List[AlunoOut])
def listar_alunos_route(db: Session = Depends(get_db), skip: int = Query(0, ge=0), limit: int = Query(100, le=100)):
    """
    Retorna uma lista de todos os alunos cadastrados.
    """
    return get_alunos(db=db, skip=skip, limit=limit)

@router.get("/{aluno_id}", response_model=AlunoOut)
def get_aluno_route(aluno_id: int, db: Session = Depends(get_db)):
    """
    Retorna as informações de um aluno específico pelo seu ID.
    """
    db_aluno = get_aluno(db, aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db_aluno

@router.put("/{aluno_id}", response_model=AlunoOut)
def atualizar_aluno_route(
    aluno_id: int, 
    aluno_update: AlunoUpdate, 
    db: Session = Depends(get_db), 
    _ = Depends(coordenador_required)
):
    """
    Atualiza as informações de um aluno existente.
    """
    db_aluno = atualizar_aluno(db, aluno_id, aluno_update)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db_aluno

@router.delete("/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_aluno_route(aluno_id: int, db: Session = Depends(get_db), _ = Depends(coordenador_required)):
    """
    Deleta um aluno do banco de dados pelo seu ID.
    """
    success = deletar_aluno(db, aluno_id)
    if not success:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return None

@router.delete("/{aluno_id}/turma", status_code=status.HTTP_200_OK, response_model=AlunoOut)
def remover_aluno_de_sua_turma_route(
    aluno_id: int,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
    aluno_atualizado = remover_aluno_da_turma(db, aluno_id=aluno_id)
    
    if not aluno_atualizado:
        raise HTTPException(status_code=404, detail="Aluno não encontrado.")
    
    return aluno_atualizado

@router.get("/documentos/{documento_id}/download")
def download_documento_route(
    documento_id: int,
    db: Session = Depends(get_db),
    _ = Depends(coordenador_required)
):
   
    db_documento = get_documento(db, documento_id)
    if not db_documento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registro de documento não encontrado.")
    
    # 2. Verifica se o arquivo físico realmente existe no caminho salvo
    caminho_arquivo = db_documento.caminho_arquivo
    if not os.path.exists(caminho_arquivo):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Arquivo não encontrado no servidor. Contate o administrador.")

    # 3. Retorna o arquivo como uma resposta de download
    return FileResponse(
        path=caminho_arquivo,
        media_type='application/octet-stream', # Um tipo genérico para downloads
        filename=db_documento.nome_arquivo   # O nome original que o arquivo terá ao ser baixado
    )
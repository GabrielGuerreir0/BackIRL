from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_access_token
from sqlalchemy.orm import Session
from db.session import SessionLocal
""" from api.deps import verificar_se_e_educador_da_turma """
from typing import List
from datetime import date
import crud.RegistroFrequencia as crud_frequencia
import schemas.RegistroFrequencia as schemas

router = APIRouter()

bearer_scheme = HTTPBearer()
def user_required(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Apenas pessoas autenticadas podem acessar esta rota."
        )
    user_role = payload.get("role")
    allowed_roles = ["educador", "coordenador", "assistente_social"]
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Acesso negado. A sua role ('{user_role}') não tem permissão para este recurso."
        )
    return payload

def educador_turma_required(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "educador" :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Apenas pessoas autenticadas podem acessar esta rota."
        )
    return payload

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/turma/{turma_id}/dia/{data}", status_code=status.HTTP_201_CREATED, dependencies=[Depends(educador_turma_required)])
def registrar_frequencia_turma(turma_id: int, data: date, payload: schemas.FrequenciaCreateList, db: Session = Depends(get_db)):
    crud_frequencia.upsert_frequencia_batch(db=db, turma_id=turma_id, data=data, frequencias=payload.frequencias)
    return {"message": "Frequência registrada com sucesso."}


@router.get(
    "/turma/{turma_id}/dia/{data}", 
    response_model=List[schemas.FrequenciaAlunoResponse], 
    summary="Consultar a lista de frequência de uma turma em um dia",
    dependencies=[Depends(user_required)]
)
def ler_frequencia_do_dia(
    turma_id: int, 
    data: date, 
    db: Session = Depends(get_db)
):
    registros = crud_frequencia.get_frequencia_by_turma_and_dia(db=db, turma_id=turma_id, data=data)
    return [
        schemas.FrequenciaAlunoResponse(
            aluno_id=reg.aluno.id,
            nome_completo=reg.aluno.nome,
            data=reg.data,
            status=reg.status.value
        ) for reg in registros
    ]


@router.get(
    "/turma/frequencia/{turma_id}",
    response_model=List[schemas.FrequenciaAlunoResponse],
    summary="Consultar o histórico de frequência completo de uma turma",
    dependencies=[Depends(user_required)]
)
def ler_historico_completo_da_turma(turma_id: int, db: Session = Depends(get_db)):
    registros_historico = crud_frequencia.get_historico_completo_por_turma(db=db, turma_id=turma_id)
    response = [
        schemas.FrequenciaAlunoResponse(
            aluno_id=reg.aluno.id,
            nome_completo=reg.aluno.nome,
            data=reg.data,
            status=reg.status.value
        ) for reg in registros_historico
    ]
    
    return response



@router.get(
    "/turma/{turma_id}/intervalo",
    response_model=List[schemas.FrequenciaAlunoResponse],
    summary="Consultar frequência de uma turma por intervalo de datas",
    dependencies=[Depends(user_required)]
)
def ler_frequencia_por_intervalo(
    turma_id: int, 
    data_inicio: date = Query(..., description="Data de início no formato AAAA-MM-DD"),
    data_fim: date = Query(..., description="Data de fim no formato AAAA-MM-DD"),
    db: Session = Depends(get_db)
):
    registros_intervalo = crud_frequencia.get_frequencia_por_turma_e_intervalo_de_datas(
        db=db, 
        turma_id=turma_id, 
        data_inicio=data_inicio, 
        data_fim=data_fim
    )
    
    response = [
        schemas.FrequenciaAlunoResponse(
            aluno_id=reg.aluno.id,
            nome_completo=reg.aluno.nome,
            data=reg.data,
            status=reg.status.value
        ) for reg in registros_intervalo
    ]
    
    return response

@router.get("/turma/{turma_id}/dia/{data}", response_model=List[schemas.FrequenciaAlunoResponse], dependencies=[Depends(user_required)])
def ler_frequencia_do_dia(turma_id: int, data: date, db: Session = Depends(get_db)):
    registros = crud_frequencia.get_frequencia_by_turma_and_dia(db=db, turma_id=turma_id, data=data)
    return [schemas.FrequenciaAlunoResponse(aluno_id=reg.aluno.id, nome_completo=reg.aluno.nome, status=reg.status.value) for reg in registros]


@router.get("/aluno/{aluno_id}", response_model=List[schemas.FrequenciaHistoricoAluno], dependencies=[Depends(user_required)])
def ler_historico_do_aluno(aluno_id: int, db: Session = Depends(get_db)):
    registros = crud_frequencia.get_historico_frequencia_by_aluno(db, aluno_id=aluno_id)
    return [schemas.FrequenciaHistoricoAluno(data=reg.data, status=reg.status.value, turma_nome=reg.turma.nome) for reg in registros]

@router.get("/aluno/{aluno_id}/dia/{data}", response_model=schemas.Frequencia, dependencies=[Depends(user_required)])
def ler_frequencia_aluno_dia(aluno_id: int, data: date, db: Session = Depends(get_db)):
    registro = crud_frequencia.get_frequencia_by_aluno_and_dia(db, aluno_id=aluno_id, data=data)
    if not registro: raise HTTPException(status_code=404, detail="Registro não encontrado para este aluno nesta data.")
    return registro
# /routers/relatorio_assistente.py

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.security import decode_access_token

from db.session import get_db
from schemas.relatorio_assistente import RelatorioCreate, RelatorioUpdate, RelatorioOut
from crud import relatorio_assistente as crud_relatorio
from crud import assistente_social as crud_assistente
from models.assistente_social import Assistente

bearer_scheme = HTTPBearer()

# --- Funções de Segurança Ajustadas ---

def coordenador_or_assistente_required(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Esta função apenas verifica o 'role' no token. 
    Perfeita para as rotas GET que não precisam do objeto do usuário.
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    allowed_roles = ["coordenador", "assistente"]
    if not payload or payload.get("role") not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a Coordenadores ou Assistentes."
        )
    return payload

def get_current_assistente_from_db(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> Assistente:
 
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "assistente":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a Assistentes."
        )
    
    user_email = payload.get("sub")
    print(user_email)
    if not user_email:
        raise HTTPException(status_code=401, detail="Token inválido: 'sub' não encontrado.")

    # 2. Busca do usuário no banco de dados
    user = crud_assistente.get_assistente_by_email(db, email=user_email)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário assistente não encontrado no banco de dados.")
        
    print(user)
    return user


router = APIRouter()


@router.post("/", response_model=RelatorioOut, status_code=status.HTTP_201_CREATED)
def criar_novo_relatorio(
    relatorio: RelatorioCreate,
    db: Session = Depends(get_db),
    current_assistente: Assistente = Depends(get_current_assistente_from_db)
):
    try:
        db_relatorio = crud_relatorio.criar_relatorio(
            db=db, relatorio=relatorio, assistente_id=current_assistente.id
        )
        if db_relatorio is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aluno com ID {relatorio.aluno_id} não encontrado."
            )
        return db_relatorio

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno no servidor. Causa: {type(e).__name__}"
        )


@router.get("/", response_model=List[RelatorioOut])
def listar_todos_os_relatorios(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0),
    # ✅ GETs usam a verificação simples, pois não precisam do objeto do usuário
    payload: dict = Depends(coordenador_or_assistente_required)
):
    """Lista todos os relatórios. Coordenadores e Assistentes."""
    return crud_relatorio.get_relatorios(db, skip=skip, limit=limit)


@router.get("/aluno/{aluno_id}", response_model=List[RelatorioOut])
def listar_relatorios_do_aluno(
    aluno_id: int,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=0),
    payload: dict = Depends(coordenador_or_assistente_required)
):
    """Lista relatórios de um aluno. Coordenadores e Assistentes."""
    return crud_relatorio.get_relatorios_por_aluno(db, aluno_id=aluno_id, skip=skip, limit=limit)


@router.get("/{relatorio_id}", response_model=RelatorioOut)
def obter_relatorio(
    relatorio_id: int, 
    db: Session = Depends(get_db),
    payload: dict = Depends(coordenador_or_assistente_required)
):
    """Obtém um relatório. Coordenadores e Assistentes."""
    db_relatorio = crud_relatorio.get_relatorio(db, relatorio_id=relatorio_id)
    if db_relatorio is None:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    return db_relatorio


@router.put("/{relatorio_id}", response_model=RelatorioOut)
def atualizar_um_relatorio(
    relatorio_id: int,
    relatorio_update: RelatorioUpdate,
    db: Session = Depends(get_db),
    # ✅ Usamos a dependência que busca o assistente no banco
    current_assistente: Assistente = Depends(get_current_assistente_from_db)
):
    """Atualiza um relatório. Somente o autor, que deve ser um assistente."""
    db_relatorio = crud_relatorio.get_relatorio(db, relatorio_id=relatorio_id)
    if not db_relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    if db_relatorio.assistente_id != current_assistente.id:
        raise HTTPException(status_code=403, detail="Apenas o autor pode editar este relatório")
        
    return crud_relatorio.atualizar_relatorio(db=db, relatorio_id=relatorio_id, relatorio_update=relatorio_update)


@router.delete("/{relatorio_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_um_relatorio(
    relatorio_id: int,
    db: Session = Depends(get_db),
    # ✅ Usamos a dependência que busca o assistente no banco
    current_assistente: Assistente = Depends(get_current_assistente_from_db)
):
    """Deleta um relatório. Somente o autor, que deve ser um assistente."""
    db_relatorio = crud_relatorio.get_relatorio(db, relatorio_id=relatorio_id)
    if not db_relatorio:
        raise HTTPException(status_code=404, detail="Relatório não encontrado")
    
    if db_relatorio.assistente_id != current_assistente.id:
        raise HTTPException(status_code=403, detail="Apenas o autor pode deletar este relatório")
        
    crud_relatorio.deletar_relatorio(db=db, relatorio_id=relatorio_id)
    return None
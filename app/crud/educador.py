from sqlalchemy.orm import Session, joinedload
from models.educador import Educador
from schemas.educador import EducadorCreate, EducadorOut, EducadorUpdate
from core.security import hash_password, verify_password
from fastapi import HTTPException

def criar_educador(db: Session, educador: EducadorCreate):
    hashed_pw = hash_password(educador.password)
    db_educador = Educador(
        nome=educador.nome,
        email=educador.email,
        telefone=educador.telefone,
        data_nascimento=educador.data_nascimento,
        hashed_password=hashed_pw
    )
    db.add(db_educador)
    db.commit()
    db.refresh(db_educador)
    return db_educador

def listar_educadores(db: Session):
    """
    Lista todos os educadores com suas turmas associadas.
    """
    educadores = db.query(Educador).options(
        joinedload(Educador.turma)
    ).all()
    
    # Força o carregamento da turma para cada educador
    for educador in educadores:
        _ = educador.turma  # Isso força o carregamento do relacionamento
    
    return educadores

def autenticar_educador(db: Session, email: str, password: str):
    educador = db.query(Educador).filter(Educador.email == email).first()
    if not educador:
        return None
    if not verify_password(password, educador.hashed_password):
        return None
    return educador

def verificar_disponibilidade_educador(db: Session, educador_id: int) -> bool:
    """
    Verifica se um educador já está associado a alguma turma.
    
    Args:
        db (Session): A sessão do banco de dados.
        educador_id (int): O ID do educador a ser verificado.
    
    Returns:
        bool: True se o educador está disponível, False caso contrário.
    """
    educador = db.query(Educador).options(
        joinedload(Educador.turma)
    ).filter(Educador.id == educador_id).first()
    
    if not educador:
        raise HTTPException(status_code=404, detail="Educador não encontrado")
    
    return educador.turma is None

def atualizar_educador(db: Session, educador_id: int, educador_update: EducadorUpdate):
    """
    Atualiza um educador no banco de dados.

    Args:
        db (Session): A sessão do banco de dados.
        educador_id (int): O ID do educador a ser atualizado.
        educador_update (EducadorUpdateSchema): O objeto Pydantic com os dados para atualização.

    Returns:
        Educador: O objeto educador atualizado ou None se não for encontrado.
    """
    # 1. Busca o objeto no banco de dados
    db_educador = db.query(Educador).filter(Educador.id == educador_id).first()
    
    if not db_educador:
        return None

    # 2. Converte o modelo Pydantic em um dicionário
    #    'exclude_unset=True' garante que apenas os campos enviados na requisição serão atualizados
    update_data = educador_update.model_dump(exclude_unset=True)

    # 3. Itera sobre os dados e atualiza o objeto do banco
    for key, value in update_data.items():
        # Trata o campo de senha de forma especial para aplicar o hash
        if key == 'password' and value:
            setattr(db_educador, 'hashed_password', hash_password(value))
        else:
            # Define o atributo no objeto do banco de dados
            setattr(db_educador, key, value)
    
    # 4. Salva as alterações e atualiza a instância
    db.commit()
    db.refresh(db_educador)
    
    return db_educador

def deletar_educador(db: Session, educador_id: int):
    educador = db.query(Educador).filter(Educador.id == educador_id).first()
    if not educador:
        return False
    db.delete(educador)
    db.commit()
    return True
def get_educador(db: Session, educador_id: int):
    return db.query(Educador).options(joinedload(Educador.turma)).filter(Educador.id == educador_id).first()

def get_educador_by_email(db: Session, email: str):
    return db.query(Educador).options(joinedload(Educador.turma)).filter(Educador.email == email).first()
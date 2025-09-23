from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random
import string
from fastapi import HTTPException
from services.email import enviar_email_recuperacao
from models.educador import Educador
from models.coordenador import Coordenador
from models.assistente_social import Assistente
from core.security import hash_password

def gerar_codigo_recuperacao(length: int = 6) -> str:
    """Gera um código de recuperação aleatório."""
    caracteres = string.ascii_uppercase + string.digits
    return ''.join(random.choice(caracteres) for _ in range(length))

async def iniciar_recuperacao_senha(db: Session, email: str):
    """
    Função unificada para iniciar o processo de recuperação de senha.
    Verifica o email em todas as roles e envia o código se encontrar.
    """
    roles = [
        (Educador, "Educador"),
        (Coordenador, "Coordenador"),
        (Assistente, "Assistente Social")
    ]
    
    for model_class, role_name in roles:
        usuario = db.query(model_class).filter(model_class.email == email).first()
        if usuario:
            codigo = gerar_codigo_recuperacao()
            usuario.codigo_recuperacao = codigo
            usuario.codigo_recuperacao_expiracao = datetime.now() + timedelta(minutes=30)
            
            db.commit()
            
            # Envia o email com o código
            await enviar_email_recuperacao(
                email=email,
                codigo=codigo,
                nome=usuario.nome if hasattr(usuario, 'nome') else usuario.name
            )
            
            return True
    
    # Se não encontrou o email em nenhuma role, retorna False
    # mas não levanta erro para não revelar se o email existe ou não
    return False

def validar_codigo(db: Session, email: str, codigo: str):
    """Função unificada para validar código de recuperação."""
    roles = [
        (Educador, "Educador"),
        (Coordenador, "Coordenador"),
        (Assistente, "Assistente Social")
    ]
    
    for model_class, _ in roles:
        usuario = db.query(model_class).filter(model_class.email == email).first()
        if usuario:
            if not usuario.codigo_recuperacao or not usuario.codigo_recuperacao_expiracao:
                raise HTTPException(status_code=400, detail="Nenhum código de recuperação solicitado")
                
            if usuario.codigo_recuperacao_expiracao < datetime.now():
                raise HTTPException(status_code=400, detail="Código de recuperação expirado")
                
            if usuario.codigo_recuperacao != codigo:
                raise HTTPException(status_code=400, detail="Código de recuperação inválido")
                
            return model_class, usuario
    
    raise HTTPException(status_code=404, detail="Email não encontrado")

def redefinir_senha(db: Session, email: str, codigo: str, nova_senha: str):
    """Função unificada para redefinir senha."""
    model_class, usuario = validar_codigo(db, email, codigo)
    
    # Atualiza a senha
    usuario.hashed_password = hash_password(nova_senha)
    # Limpa o código de recuperação
    usuario.codigo_recuperacao = None
    usuario.codigo_recuperacao_expiracao = None
    
    db.commit()
    return True
from pydantic import BaseModel, EmailStr

class SolicitarRecuperacaoSchema(BaseModel):
    """Schema para solicitar recuperação de senha"""
    email: EmailStr

class ValidarCodigoSchema(BaseModel):
    """Schema para validar código de recuperação"""
    email: EmailStr
    codigo: str

class RedefinirSenhaSchema(BaseModel):
    """Schema para redefinir senha"""
    email: EmailStr
    codigo: str
    nova_senha: str
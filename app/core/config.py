# /core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ATENÇÃO: Gere uma chave secreta forte e a coloque em um arquivo .env
    # Comando para gerar no terminal: openssl rand -hex 32
    SECRET_KEY: str = "sua_chave_secreta_supersegura"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 # O token expira em 1 hora
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30 # O refresh token expira em 30 dias

    # Configurações de Email
    SMTP_HOST: str = "smtp.gmail.com"  # Exemplo para Gmail
    SMTP_PORT: int = 587
    SMTP_USER: str = "seu_email@gmail.com"
    SMTP_PASSWORD: str = "sua_senha_de_app"
    SMTP_FROM: str = "seu_email@gmail.com"

    class Config:
        env_file = ".env"

settings = Settings()
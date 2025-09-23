from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from typing import List
from core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.SMTP_USER,
    MAIL_PASSWORD=settings.SMTP_PASSWORD,
    MAIL_FROM=settings.SMTP_FROM,
    MAIL_PORT=settings.SMTP_PORT,
    MAIL_SERVER=settings.SMTP_HOST,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def enviar_email_recuperacao(email: EmailStr, codigo: str, nome: str):
    """
    Envia email com código de recuperação de senha.
    """
    html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
            <h3 style="color: #2c3e50; text-align: center; border-bottom: 2px solid #3498db; padding-bottom: 10px;">Recuperação de Senha - IRL</h3>
            <p style="color: #34495e;">Olá {nome},</p>
            <p style="color: #34495e;">Você solicitou a recuperação de senha. Use o código abaixo para redefinir sua senha:</p>
            <div style="text-align: center; margin: 25px 0;">
                <h2 style="font-size: 32px; letter-spacing: 5px; color: #3498db; background: #f8f9fa; padding: 15px; border-radius: 5px; display: inline-block;">{codigo}</h2>
            </div>
            <p style="color: #e74c3c; font-size: 14px;">Este código expira em 30 minutos.</p>
            <p style="color: #7f8c8d; font-size: 14px; border-top: 1px solid #eee; margin-top: 20px; padding-top: 20px;">Se você não solicitou a recuperação de senha, ignore este email.</p>
            <div style="text-align: center; margin-top: 20px; font-size: 12px; color: #95a5a6;">
                <p>Este é um email automático, por favor não responda.</p>
            </div>
        </div>
    """

    message = MessageSchema(
        subject="Recuperação de Senha - IRL",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)
from fastapi import FastAPI
from api.v1 import (
    coordenador, educador, aluno, turma, dashboard, planejamento,
    assistente_social, login, RegistroFrequencia, relatorios,
    relatorio_assistente, recuperacao_senha
)
from db.session import engine
from db.base import Base
from fastapi.middleware.cors import CORSMiddleware



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Educacional")


# Lista de origens permitidas
origins = [
    "http://localhost:5173",  # Mantenha as de localhost para facilitar o desenvolvimento futuro
    "https://eduirl.site",      # <-- A ORIGEM QUE FALTAVA
    "https://www.eduirl.site",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(coordenador.router, prefix="/api/v1/coordenadores", tags=["Coordenadores"])
app.include_router(educador.router, prefix="/api/v1/educadores", tags=["Educadores"])
app.include_router(aluno.router, prefix="/api/v1/alunos", tags=["Alunos"])
app.include_router(turma.router, prefix="/api/v1/turma", tags=["turma"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])
app.include_router(planejamento.router, prefix="/api/v1/planejamentos", tags=["Planejamentos"])
app.include_router(assistente_social.router, prefix="/api/v1/assistente", tags=["Assistente Social"])
app.include_router(login.router, prefix="/api/v1/login", tags=["Login"])
app.include_router(RegistroFrequencia.router, prefix="/api/v1", tags=["Frequencia"])
app.include_router(relatorios.router, prefix="/api/v1/relatorio", tags=["Relatorio"])
app.include_router(relatorio_assistente.router, prefix="/api/v1/relatorio-assistente", tags=["Relatorio Assistente"])
app.include_router(recuperacao_senha.router)
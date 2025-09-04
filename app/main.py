from fastapi import FastAPI
from api.v1 import coordenador, educador, aluno, turma, dashboard, planejamento, assistente_social, login
from db.session import engine
from db.base import Base
from fastapi.middleware.cors import CORSMiddleware



Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema Educacional")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:5174", "http://localhost:8080", "http://localhost:4200", "http://localhost"],  
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
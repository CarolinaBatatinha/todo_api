from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import auth, todos
from app.core.database import create_tables, check_db_connection
from app.core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handler do ciclo de vida da aplicação:
    - Cria tabelas no startup
    - Executa limpeza no shutdown (se necessário)
    """
    print("Iniciando aplicação...")
    await create_tables()
    
    # Verifica conexão com o banco
    if not await check_db_connection():
        raise RuntimeError("Falha na conexão com o banco de dados")
    
    yield
    
    print("Encerrando aplicação...")
    # Adicione aqui qualquer lógica de limpeza necessária

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",  # Habilita Swagger UI em /docs
    #redoc_url="/redoc",  # Habilita ReDoc em /redoc
    openapi_url="/openapi.json"  # Endpoint para OpenAPI schema
)

# Configuração de CORS (Ajuste conforme necessidades de segurança)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota de health check
@app.get("/health", tags=["Monitoramento"])
async def health_check():
    """
    Endpoint para verificar o status da API e conexão com o banco
    """
    db_status = await check_db_connection()
    return {
        "status": "online",
        "database": "connected" if db_status else "disconnected",
        "version": settings.VERSION
    }

# Rota raiz
@app.get("/", tags=["Root"])
async def root():
    """
    Endpoint raiz com informações básicas da API
    """
    return {
        "message": f"Bem-vindo à {settings.PROJECT_NAME}",
        "docs": "/docs",
        "version": settings.VERSION
    }

# Inclusão dos routers
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticação"]
)

app.include_router(
    todos.router,
    prefix="/todos",
    tags=["Tarefas"]
)

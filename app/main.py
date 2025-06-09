from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.routes import auth, todos
from app.core.database import create_tables, check_db_connection
from app.core.config import settings
import logging

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Iniciando aplicação...")
        
        # Criar tabelas no banco de dados
        await create_tables()
        
        # Verificar conexão com o banco
        if not await check_db_connection():
            logger.error("Falha na conexão com o banco de dados")
            raise RuntimeError("Não foi possível conectar ao banco de dados")
            
        logger.info("Conexão com o banco de dados estabelecida com sucesso")
        
        yield
        
    except Exception as e:
        logger.error(f"Erro durante a inicialização: {str(e)}")
        raise
    finally:
        logger.info("Encerrando aplicação...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["Monitoramento"])
async def health_check():
    
    # Endpoint para verificar o status da API
    db_healthy = await check_db_connection()
    return JSONResponse(
        status_code=status.HTTP_200_OK if db_healthy else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "online" if db_healthy else "degraded",
            "database": "connected" if db_healthy else "disconnected",
            "version": settings.VERSION
        }
    )

@app.get("/", tags=["Root"])
async def root():
    # Endpoint raiz da API
    return {
        "message": f"Bem-vindo à {settings.PROJECT_NAME}",
        "docs": "/docs",
        "redoc": "/redoc",
        "version": settings.VERSION
    }

# Rotas de autenticação
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Autenticação"]
)

# Rotas de TODOs
app.include_router(
    todos.router,
    prefix="/todos",
    tags=["Tarefas"]
)
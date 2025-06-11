from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.core.config import settings

Base = declarative_base()

# Configuração do banco de dados SÍNCRONO
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Configuração do banco de dados ASSÍNCRONO
async_engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    pool_pre_ping=True
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Função de dependência para sessão SÍNCRONA
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função de dependência para sessão ASSÍNCRONA (corrigida)
async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db  

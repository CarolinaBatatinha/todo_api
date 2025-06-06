from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database
from app.core.config import settings

# URL do banco de dados a partir das configurações
DATABASE_URL = settings.DATABASE_URL

# Criação do engine do SQLAlchemy (para coperações síncronas, como criação de tabelas)
engine = create_engine (
    DATABASE_URL,
    pool_size=20,  # Número de conexões mantidas no pool
    max_overflow=10,  # Número máximo de conexões além do pool_size
    pool_pre_ping=True,  # Verifica a conexão antes de usá-la
    pool_recycle=3600  # Recicla conexões após 1 hora
)

# Session local para operações síncronas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Instância do Database para operações assíncronas
database = Database(DATABASE_URL)

# Base para os modelos SQLAlchemy
Base = declarative_base()

# Dependência para injeção de sessão síncrona
def get_db():
    """
    Fornece uma sessão de banco de dados para operações síncronas.
    Deve ser usada em rotas que não são assíncronas.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependência para conexão assíncrona
async def get_async_db():
    """
    Fornece uma conexão de banco de dados para operações assíncronas.
    Deve ser usada em rotas assíncronas.
    """
    await database.connect()
    try:
        yield database
    finally:
        await database.disconnect()

async def create_tables():
    """
    Cria todas as tabelas no banco de dados.
    Deve ser chamada na inicialização da aplicação.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def check_db_connection():
    """
    Verifica se a conexão com o banco de dados está ativa.
    Útil para health checks.
    """
    try:
        await database.execute("SELECT 1")
        return True
    except Exception:
        return False
    
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, FastAPI
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.database import get_async_db
from app.models.user import User

# Cria a aplicação FastAPI
app = FastAPI()

# Configurações de segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verifica se a senha corresponde ao hash
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Gera hash da senha para armazenamento seguro
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    # Cria token JWT com tempo de expiração
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_user(db: AsyncSession, email: str) -> User | None:
    # Busca usuário por email no banco de dados
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_db)
) -> User:
    # Valida token JWT e retorna usuário autenticado
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception

        user = await get_user(db, email=email)
        if not user:
            raise credentials_exception

        return user
    except JWTError:
        raise credentials_exception

# Rota raiz para verificação
@app.get("/")
async def root():
    # Endpoint de verificação de saúde da API
    return {"message": "API funcionando!", "status": "OK"}

@app.post("/auth/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    # Endpoint de login que retorna token JWT
    user = await get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

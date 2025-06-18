from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings
from app.core.database import get_async_db
from app.models.user import User
from app.routes import todos  

# Cria a aplicação FastAPI
app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="API de gerenciamento de tarefas com autenticação JWT"
)

# Inclui os routers
app.include_router(todos.router)

# Configurações de segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_user(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


todo_list = [
    {"id": 1, "tarefa": "Comprar pão", "feito": False},
    {"id": 2, "tarefa": "Estudar FastAPI", "feito": True},
    {"id": 3, "tarefa": "Fazer exercícios", "feito": False},
]
# Rota raiz de teste
@app.get("/")
async def root():
    return {"message": "API funcionando!", "status": "OK"}


# Endpoint de login JWT
@app.post("/auth/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db)
):
    user = await get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )

    access_token = create_access_token(data={'sub': user.email})
    return {"access_token": access_token, 'token_type': 'bearer'}

# Nova rota: GET /todos
@app.get("/todos")
def get_todos():
    return todo_list

# Endpoint para frontend
app.mount("/static", StaticFiles(directory='static'), name='static')

@app.get('/home', response_class=HTMLResponse)
async def read_home():
    return '''
    <html>
        <head>
            <title>To-Do App</title>
        </head>
        <body>
            <h1>Minha Lista de Tarefas</h1>
            <div id="todos"></div>
            <script src="/static/app.js"></script>
        </body>
    </html>
    '''
    
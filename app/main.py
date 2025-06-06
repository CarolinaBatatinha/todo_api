from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, todos 
from app.core.database import Base, engine

app = FastAPI(
    title = 'To-do API',
    description='API para gerenciamento de tarefas com autenticação JWT',
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins =['*'],
    allow_credentials=False,
    allow_methods=['GET', 'POST', 'PUT','DELETE'],
    # allow_headers=['Content-Type', 'Authorization']
)

@app.get('/')
def read_root():
    return {'message': 'Todo API está funcionando'}

@app.on_event('startup')
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
# Inclusão dos routers
app.include_router(auth.router)
app.include_router(todos.router, prefix='/todos', tags=['todos'])

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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
    return {"message": "Todo API está funcionando"}

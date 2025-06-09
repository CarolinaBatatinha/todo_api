from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.todo import Todo
from app.models.user import User
from app.schemas.todo import TodoCreate, Todo as TodoSchema
from app.core.database import get_db
from app.core.security import get_current_user

# Cria um roteador para as rotas de TODO
router = APIRouter(prefix='/todos', tags=['todos'])

# Rota para criar um novo TODO
@router.post('/', response_model=TodoSchema, status_code=201)
def create_todo(
    todo: TodoCreate,  # Dados do TODO vindos do corpo da requisição
    db: Session = Depends(get_db),  # Sessão do banco de dados
    current_user: User = Depends(get_current_user)  # Usuário autenticado
):

    # Cria uma instância do TODO associada ao usuário atual
    db_todo = Todo(**todo.dict(), owner_id=current_user.id)
    
    # Adiciona ao banco de dados
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    
    return db_todo

# Rota para listar TODOs do usuário
@router.get('/', response_model=List[TodoSchema])
def read_todos(
    skip: int = 0,  # Paginação - quantos itens pular
    limit: int = 100,  # Paginação - limite de itens por página
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Busca os TODOs filtrando pelo dono e aplicando paginação
    todos = db.query(Todo).filter(
        Todo.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return todos

# Rota para buscar um TODO específico
@router.get('/{todo_id}', response_model=TodoSchema)
def read_todo(
    todo_id: int,  # ID do TODO a ser buscado
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Busca o TODO verificando o ID e o dono
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=404,
            detail='TODO não encontrado ou você não tem permissão para acessá-lo'
        )
    
    return todo

# Rota para atualizar um TODO
@router.put('/{todo_id}', response_model=TodoSchema)
def update_todo(
    todo_id: int,  # ID do TODO a ser atualizado
    todo: TodoCreate,  # Novos dados do TODO
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Busca o TODO existente
    db_todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == current_user.id
    ).first()
    
    if not db_todo:
        raise HTTPException(
            status_code=404,
            detail='TODO não encontrado ou você não tem permissão para editá-lo'
        )
    
    # Atualiza os campos do TODO
    for key, value in todo.dict().items():
        setattr(db_todo, key, value)
    
    db.commit()
    db.refresh(db_todo)
    
    return db_todo

# Rota para deletar um TODO
@router.delete('/{todo_id}')
def delete_todo(
    todo_id: int,  # ID do TODO a ser deletado
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Busca o TODO para deletar
    todo = db.query(Todo).filter(
        Todo.id == todo_id,
        Todo.owner_id == current_user.id
    ).first()
    
    if not todo:
        raise HTTPException(
            status_code=404,
            detail='TODO não encontrado ou você não tem permissão para removê-lo'
        )
    
    # Remove o TODO
    db.delete(todo)
    db.commit()
    
    return {'message': 'TODO removido com sucesso'}

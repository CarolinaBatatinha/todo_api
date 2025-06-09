# API de tarefas (*to-do list*)

Projeto em desenvolvimento com o propósito de aprendizado.

## Para rodar

Dentro do ambiente virtualizado, instalar as seguintes dependências:
```bash
pip install fastapi 'uvicorn[standard]' 'python-jose[cryptography]' 'passlib[bcrypt]' python-multipart pydantic-settings

# Para os testes unitários
pip install pytest pytest-cov httpx

# Para o banco de dados
pip install sqlalchemy 'databases[postgresql]'
```
## Estrutura do projeto

Criada para facilitar a manutenção e escalabilidade.

```
todo_api/
├── app/                  # Código principal da aplicação
│   ├── __init__.py
│   ├── main.py           # Ponto de entrada
│   ├── models/           # Modelos de dados
│   ├── schemas/          # Esquemas Pydantic
│   ├── routes/           # Rotas da API
│   ├── core/             # Configurações centrais
│   └── utils/            # Utilitários
├── tests/                # Testes unitários
├── Dockerfile            # Configuração do Docker
├── requirements.txt      # Dependências
└── .venv                  # Variáveis de ambiente
```




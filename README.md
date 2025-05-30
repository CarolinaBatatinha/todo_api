# API de tarefas (*to-do list*)


## Estrutura do projeto
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
└── .env                  # Variáveis de ambiente
```
```bash
pip install fastapi "uvicorn[standard]" "python-jose[cryptography]" "passlib[bcrypt]" python-multipart pydantic-settings
# Para os testes unitários
pip install pytest pytest-cov httpx
```



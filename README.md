# 📝 API de Tarefas (To-Do List)

Projeto ***em construção*** com o propósito de aprendizado em **FastAPI**, arquitetura escalável e boas práticas no desenvolvimento de APIs RESTful.

---

## 🚀 Funcionalidades

- ✅ Cadastro e autenticação de usuários (JWT)
- 📝 CRUD de tarefas (create, read, update, delete)
- 🔐 Rotas protegidas por autenticação
- 🗃️ Integração com banco de dados PostgreSQL via SQLAlchemy
- ✅ Testes unitários com cobertura (*a desenvolver*)

---

## ⚙️ Requisitos

- Python 3.10+
- PostgreSQL
- [Poetry](https://python-poetry.org/) ou `venv` (opcional)
- Docker (opcional)

---

## 💻 Como Rodar Localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/CarolinaBatatinha/todo_api.git
   cd todo_api
    ```
2. Crie e ative o ambiente virtual:
   
   ```bash
    python -m venv .venv
    source .venv/bin/activate  # ou .venv\Scripts\activate no Windows
   ```
3. Instale as dependências

    ```bash
    pip install -r requirements.txt
    ```

# Para o banco de dados
```
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


## 📄 Licença

Este projeto é de código aberto, desenvolvido para fins de estudo. Você pode usá-lo, modificá-lo e redistribuí-lo conforme desejar.
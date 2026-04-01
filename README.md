# ✂️ HairTime - Gestão de Agendamentos

O **HairTime** é uma solução moderna e premium para a gestão de barbearias e salões de beleza. O sistema permite que clientes realizem agendamentos online de forma intuitiva, enquanto profissionais acompanham sua agenda em tempo real através de um dashboard exclusivo.

## ✨ Funcionalidades

* **Agendamento Online**: Escolha de serviços, data e horários disponíveis com validação em tempo real.
* **Dashboard do Profissional**: Visualização clara de métricas (total, confirmados, pendentes) e lista detalhada de compromissos.
* **Sistema de Autenticação**: Cadastro e login de usuários (Clientes e Barbeiros) com segurança via JWT.
* **Design Premium**: Interface escura com detalhes em dourado, focada na experiência do usuário e responsividade.

## 🛠️ Tecnologias Utilizadas

### Front-end
* **Vue 3** (Composition API)
* **TypeScript**
* **Vite**
* **Vue Router**

### Back-end
* **FastAPI** (Python)
* **SQLAlchemy** (ORM)
* **SQLite** (Banco de dados local)
* **PyJWT** (Tokens de autenticação)

## 🚀 Como rodar o projeto

Para rodar o HairTime localmente, siga os passos abaixo:

### 1. Pré-requisitos
* Node.js instalado
* Python 3.10+ instalado

### 2. Configurando o Back-end

    # Entre na pasta do back-end
    cd sprint_1/back-end

    # Crie e ative o ambiente virtual (Windows)
    python -m venv venv
    .\venv\Scripts\activate

    # Instale as dependências necessárias
    pip install fastapi uvicorn sqlalchemy pyjwt

    # Inicie o servidor
    uvicorn main:app --reload

O servidor estará rodando em: `http://localhost:8000`

### 3. Configurando o Front-end

    # Em um novo terminal, entre na pasta do front-end
    cd sprint_1/front-end

    # Instale as dependências do Node
    npm install

    # Inicie o projeto em modo de desenvolvimento
    npm run dev

O site estará disponível em: `http://localhost:5173`

## 📌 Estrutura de Pastas Principal
* `/src/services/api.ts`: Configuração das chamadas HTTP e rotas da API.
* `/src/composables`: Lógica de estado global (Auth e Agendamento).
* `/src/views`: Telas (pages) principais do sistema.
* `main.py`: Definição das rotas e lógica do servidor FastAPI.
* `models.py`: Mapeamento das tabelas do banco de dados.

---
Desenvolvido por **Bruno** 
Desenvolvido por **Livia** 
Desenvolvido por **Miguel** 
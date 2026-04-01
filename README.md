# ENG_SOFTWARE
Repositório da disciplina Eng. de Software

✂️ HairTime - Gestão de Agendamentos

O HairTime é uma solução moderna e "premium" para a gestão de barbearias e salões de beleza. O sistema permite que clientes realizem agendamentos online de forma intuitiva, enquanto profissionais acompanham sua agenda em tempo real através de um dashboard exclusivo.

✨ Funcionalidades
Agendamento Online: Escolha de serviços, data e horários disponíveis com validação em tempo real.

Dashboard do Profissional: Visualização clara de métricas (total, confirmados, pendentes) e lista detalhada de compromissos.

Sistema de Autenticação: Cadastro e login de usuários (Clientes e Barbeiros) com segurança via JWT.

Design Premium: Interface escura com detalhes em dourado, focada na experiência do usuário e responsividade.

🛠️ Tecnologias Utilizadas
Front-end
Vue 3 (Composition API)

TypeScript

Vite

Vue Router

Back-end
FastAPI (Python)

SQLAlchemy (ORM)

SQLite (Banco de dados local)

PyJWT (Tokens de autenticação)

🚀 Como rodar o projeto
Para rodar o HairTime localmente, siga os passos abaixo:

1. Pré-requisitos
Node.js instalado

Python 3.10+ instalado

2. Configurando o Back-end
Bash

# Entre na pasta do back-end
cd back-end

# Crie e ative o ambiente virtual (Windows)
python -m venv venv
.\venv\Scripts\activate

# Instale as dependências
pip install fastapi uvicorn sqlalchemy pyjwt

# Inicie o servidor
uvicorn main:app --reload
O servidor estará rodando em: http://localhost:8000.

3. Configurando o Front-end
Bash

# Em um novo terminal, entre na pasta do front-end
cd front-end

# Instale as dependências
npm install

# Inicie o projeto
npm run dev
O site estará disponível em: http://localhost:5173.

📌 Estrutura de Pastas
/src/services/api.ts: Configuração das chamadas HTTP.

/src/composables: Lógica de estado (Auth e Agendamento).

/src/views: Telas principais do sistema.

main.py: Rotas e lógica do servidor FastAPI.

models.py: Definição das tabelas do banco de dados.
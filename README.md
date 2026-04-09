# ✂️ HairTime - Gestão de Agendamentos

O **HairTime** é uma solução moderna e premium para a gestão de barbearias e salões de beleza. O sistema permite que clientes realizem agendamentos online de forma intuitiva, enquanto profissionais acompanham sua agenda em tempo real através de um dashboard exclusivo.

## 🌍 Links do Projeto
* **Site (Front-end):** [https://hairtime-kappa.vercel.app](https://hairtime-kappa.vercel.app)
* **API (Back-end):** [https://eng-software-i94g.onrender.com/docs](https://eng-software-i94g.onrender.com/docs)

## ✨ Funcionalidades
* **Agendamento Online**: Escolha de serviços, data e horários disponíveis com validação em tempo real.
* **Dashboard do Profissional**: Visualização de métricas (total, confirmados e pendentes) e lista de compromissos.
* **Segurança**: Criptografia de senhas via hash e autenticação robusta com JWT.
* **Design Premium**: Interface Dark moderna e responsiva desenvolvida com Vue 3.

## 🛠️ Tecnologias Utilizadas

### Front-end
* **Vue 3** (Composition API)
* **TypeScript** (Tipagem estática para maior segurança)
* **Vite** (Ferramenta de build rápida)
* **Vue Router** (Gerenciamento de rotas e navegação)

### Back-end
* **FastAPI** (Python) - Framework de alta performance
* **SQLAlchemy** (ORM) - Abstração e gestão do banco de dados
* **PostgreSQL** (Hospedado via Supabase)
* **Passlib / Bcrypt** (Criptografia segura de senhas)
* **PyJWT** (Gerenciamento de tokens de sessão)

## ☁️ Arquitetura de Nuvem (Deploy)
O sistema opera em uma infraestrutura distribuída em nuvem para garantir alta disponibilidade:
* **Vercel**: Hospedagem do Front-end com integração contínua (CI/CD).
* **Render**: Servidor de aplicação para o Back-end Python.
* **Supabase**: Instância de banco de dados relacional PostgreSQL.

## 📌 Estrutura de Projeto
* `/front-end/src/views`: Telas e páginas principais do sistema.
* `/front-end/src/composables`: Lógica de negócio e gerenciamento de estado global.
* `/front-end/src/services/api.ts`: Centralização das chamadas HTTP para a API externa.
* `/back-end/main.py`: Ponto de entrada da API e configuração de middlewares (CORS).
* `/back-end/models.py`: Definição das classes e tabelas do banco de dados.
* `/back-end/database.py`: Configuração da conexão com o banco de dados remoto.

---
Desenvolvido por **Bruno**, **Livia** e **Miguel**.

integração com jira

## 🎯 Relacionado à Tarefa
Fixes #SCRUM-5

## 🚀 O que foi feito nesta Sprint?
- Implementação da rota de cadastro de usuários no FastAPI.
- Integração do Front-end (Vue 3 + Composition API) com o endpoint de registro.
- Configuração de Hash de senha (Bcrypt) para segurança dos dados sensíveis.
- CI/CD e Deploy realizados com sucesso no Render e Vercel.

## ✅ Definição de Pronto (DoD) atendida:
- [x] Usuário consegue se cadastrar na plataforma.
- [x] Dados persistidos com segurança no PostgreSQL (Supabase).
- [x] Documentação interativa (Swagger) atualizada e testável.
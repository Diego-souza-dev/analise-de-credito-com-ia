# analise-de-credito-com-ia
sistema backend com integração de IA e FastAPI para analise de credito fixa ou aleatoria.
# Motor de Análise de Risco de Crédito com IA 🏦🤖

API desenvolvida em Python para simular a avaliação de crédito de clientes em instituições financeiras. O sistema utiliza Inteligência Artificial Generativa para analisar o perfil financeiro do solicitante e emitir um parecer de aprovação ou reprovação, acompanhado de uma justificativa técnica e dicas de educação financeira.

## 🚀 Tecnologias Utilizadas
- **Python 3**
- **FastAPI** (Framework moderno e assíncrono para APIs)
- **Google Gemini API** (Integração com LLM para tomada de decisão)
- **Pydantic** (Validação e tipagem rigorosa de dados)
- **Uvicorn** (Servidor ASGI)
- **Dotenv** (Segurança de variáveis de ambiente)

## ⚙️ Funcionalidades
- `POST /analise-credito`: Recebe dados do cliente (idade, renda, score, valor solicitado) e retorna o parecer da IA.
- `GET /simular-analise`: Gera um perfil de cliente mockado (aleatório) e processa a análise automaticamente. Ideal para testar a aplicação com um clique.

## 🔗 Teste o Projeto Online
Acesse a documentação interativa (Swagger UI) e teste a API direto no navegador:
https://analise-de-credito-com-ia.onrender.com/docs

## 👨‍💻 Autor
**Diego Souza Santos**
*Estudante de Engenharia de Software com foco em Desenvolvimento Back-End (Python, Inteligencia Artificial).*

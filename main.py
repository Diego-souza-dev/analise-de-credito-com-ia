import os
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv

# 1. Configuração da IA e Segurança
load_dotenv()
CHAVE_API = os.getenv("GEMINI_API_KEY")

if not CHAVE_API:
    raise ValueError("Chave da API não encontrada. Verifique seu arquivo .env")

genai.configure(api_key=CHAVE_API)

# 2. SELEÇÃO DINÂMICA DE MODELO (Evita o Erro 404)
# O Python vai listar os modelos da sua conta e pegar o primeiro que gera texto
modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]

if not modelos_disponiveis:
    raise ValueError("Nenhum modelo de texto encontrado para esta chave de API.")

# Pega o primeiro da lista (ex: models/gemini-1.5-flash-latest, etc)
modelo_escolhido = modelos_disponiveis[0]
print(f"--- Sistema iniciado usando o modelo: {modelo_escolhido} ---")

modelo = genai.GenerativeModel(modelo_escolhido)

# 3. Inicialização da API
app = FastAPI(
    title="Motor de Análise de Risco com IA",
    description="API inteligente para avaliação de crédito em tempo real."
)



# 3. Validação de Dados (Pydantic)
# Isso garante que a API só aceite os dados no formato correto
class DadosCliente(BaseModel):
    nome: str
    idade: int
    renda_mensal: float
    valor_solicitado: float
    score_credito: int

# 4. Criação do Endpoint (Rota que recebe os dados)
@app.post("/analise-credito")
async def analisar_credito(cliente: DadosCliente):
    try:
        # Construindo o prompt: ensinando a IA a pensar como analista
        prompt = f"""
        Você é um analista de risco de crédito de uma instituição financeira.
        Analise o seguinte perfil e decida se aprova ou reprova o empréstimo.
        
        Dados do cliente:
        - Nome: {cliente.nome}
        - Idade: {cliente.idade} anos
        - Renda Mensal: R$ {cliente.renda_mensal}
        - Valor Solicitado: R$ {cliente.valor_solicitado}
        - Score de Crédito: {cliente.score_credito} (escala de 0 a 1000)

        Regras do banco:
        - O valor solicitado não deve ser excessivamente desproporcional à renda.
        - Scores abaixo de 400 são considerados de alto risco.
        
        Responda estritamente neste formato:
        STATUS: [APROVADO ou REPROVADO]
        JUSTIFICATIVA: [Sua explicação clara, técnica e empática]
        DICA FINANCEIRA: [Uma breve dica de educação financeira para o cliente]
        """

        # A mágica acontece aqui: chamamos a IA
        resposta_ia = modelo.generate_content(prompt)

        # Devolvemos a resposta estruturada para quem chamou a API
        return {
            "sucesso": True,
            "cliente": cliente.nome,
            "parecer_inteligencia_artificial": resposta_ia.text
        }
        
    except Exception as e:
        # Se a IA falhar ou a chave estiver errada, devolvemos um erro amigável
        raise HTTPException(status_code=500, detail=f"Erro no processamento da IA: {str(e)}")

# 5. Rota de Simulação Automática
@app.get("/simular-analise")
async def simular_analise_automatica():
    try:
        # 1. O Python inventa um perfil de cliente aleatório
        nomes = ["Ana", "Carlos", "Beatriz", "João", "Mariana", "Fernanda", "Pedro"]
        cliente_mock = {
            "nome": random.choice(nomes),
            "idade": random.randint(18, 65),
            "renda_mensal": round(random.uniform(1500, 15000), 2),
            "valor_solicitado": round(random.uniform(1000, 80000), 2),
            "score_credito": random.randint(200, 950)
        }

        # 2. Construímos o prompt com os dados aleatórios
        prompt = f"""
        Você é um analista de risco de crédito de uma instituição financeira.
        Analise o seguinte perfil e decida se aprova ou reprova o empréstimo.
        
        Dados do cliente:
        - Nome: {cliente_mock['nome']}
        - Idade: {cliente_mock['idade']} anos
        - Renda Mensal: R$ {cliente_mock['renda_mensal']}
        - Valor Solicitado: R$ {cliente_mock['valor_solicitado']}
        - Score de Crédito: {cliente_mock['score_credito']} (escala de 0 a 1000)

        Regras do banco:
        - O valor solicitado não deve ser excessivamente desproporcional à renda.
        - Scores abaixo de 400 são considerados de alto risco.
        
        Responda estritamente neste formato:
        STATUS: [APROVADO ou REPROVADO]
        JUSTIFICATIVA: [Sua explicação clara, técnica e empática]
        DICA FINANCEIRA: [Uma breve dica de educação financeira para o cliente]
        """

        # 3. Chamamos a IA
        resposta_ia = modelo.generate_content(prompt)

        # 4. Devolvemos os dados que foram gerados e a resposta da IA
        return {
            "sucesso": True,
            "dados_gerados_aleatoriamente": cliente_mock,
            "parecer_inteligencia_artificial": resposta_ia.text
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na simulação: {str(e)}")
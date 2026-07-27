import os
import json
import random
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ==========================================
# CONFIGURAÇÕES DA OPERAÇÃO
# ==========================================
BLOGGER_API_VERSION = "v3"
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "#")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Lista de subnichos para rotação automática
SUBNICHOS = [
    "Fones de Ouvido Bluetooth com Cancelamento de Ruído",
    "Smartwatches e Relógios Inteligentes para Treino",
    "Aspiradores de Pó Robô Inteligentes",
    "Caixas de Som Portáteis à Prova D'água",
    "Projetores Portáteis para Home Cinema",
    "Teclados Mecânicos Sem Fio para Trabalho e Jogos",
    "Air Fryers e Fritadeiras Sem Óleo"
]

PAIS = "Brasil"


def get_blogger_service():
    """Autentica na API do Blogger usando o Refresh Token."""
    credentials = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build("blogger", BLOGGER_API_VERSION, credentials=credentials)


def gerar_conteudo_gemini(subnicho, pais):
    """Gera um artigo único formatado em HTML utilizando o Gemini."""
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    Você é um redator profissional de SEO e Copywriting especializado em avaliações de produtos e marketing de afiliados.
    Escreva um artigo persuasivo e informativo sobre a escolha de produtos no subnicho '{subnicho}' focado no público de {pais}.

    Regras OBRIGATÓRIAS:
    1. Retorne a resposta estritamente em formato JSON com duas chaves: "titulo" e "conteudo_html".
    2. O conteúdo deve ser apenas o corpo do artigo formatado em HTML simples para o Blogger (use <h3>, <p>, <ul>, <li>, <strong>).
    3. NÃO inclua as tags <html>, <head>, <body> ou ```html.
    4. Adicione um Call to Action (CTA) convincente recomendando a compra e insira o seguinte link exatamente como formatado:
       <p style="text-align: center; margin: 20px 0;"><a href="{AFFILIATE_TAG}" target="_blank" rel="nofollow" style="background-color: #28a745; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">👉 Clique aqui para ver ofertas atualizadas com desconto</a></p>

    Estrutura do Artigo:
    - Título atraente otimizado para buscas no Google (SEO Long-Tail).
    - Introdução engajadora apresentando o problema ou desejo do consumidor.
    - O que considerar antes de comprar (pontos fortes, durabilidade, tecnologia).
    - Chamada para ação com o botão/link de afiliado fornecido.
    - Conclusão objetiva.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    dados = json.loads(response.text)
    return dados["titulo"], dados["conteudo_html"]


def executar_robo():
    # Validação de credenciais básicas
    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, GEMINI_API_KEY]):
        print("Erro: Uma ou mais variáveis de ambiente (Secrets) não foram configuradas no GitHub.")
        return

    # Sorteia um subnicho da lista a cada execução
    subnicho_atual = random.choice(SUBNICHOS)
    print(f"Subnicho selecionado para esta execução: {subnicho_atual}")

    try:
        # Autenticação no Blogger
        service = get_blogger_service()
        blogs = service.blogs().listByUser(userId="self").execute()
        
        if not blogs.get("items"):
            print("Erro: Nenhum blog encontrado na conta cadastrada.")
            return

        blog_id = blogs["items"][0]["id"]
        blog_nome = blogs["items"][0]["name"]
        print(f"Conectado ao blog: '{blog_nome}' (ID: {blog_id})")

        # Geração de conteúdo via Gemini
        print("Solicitando geração de artigo para a API do Gemini...")
        titulo, conteudo_html = gerar_conteudo_gemini(subnicho_atual, PAIS)

        # Publicação no Blogger
        body = {
            "title": titulo,
            "content": conteudo_html
        }

        print("Publicando artigo no Blogger...")
        post = service.posts().insert(blogId=blog_id, body=body).execute()
        print(f"🚀 Sucesso! Artigo publicado: {post.get('url')}")

    except Exception as e:
        print(f"❌ Ocorreu um erro durante a execução: {e}")


if __name__ == "__main__":
    print("--- Iniciando Robô Afiliado Global com IA Gemini ---")
    executar_robo()

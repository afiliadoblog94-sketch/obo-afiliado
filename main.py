import os
import random
import json
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# --- CONFIGURAÇÕES E VARIÁVEIS DE AMBIENTE ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

# Link de afiliado com fallback padrão
AFFILIATE_LINK = os.getenv("SMART_AFFILIATE_LINK", "https://www.amazon.com.br/?tag=meublogglobal-20")

# ID do seu Blog no Blogger
BLOG_ID = os.getenv("BLOGGER_BLOG_ID", "2641162560341629410")

# Categorias para variação diária de posts
NICHOS = [
    "Tecnologia e Eletrônicos (Smartphones, Smartwatches, Fones TWS)",
    "Casa Inteligente e Eletrodomésticos (Air Fryers, Robôs Aspiradores, Cafeteiras)",
    "Periféricos Gamer e Setup (Teclados Mecânicos, Mouses, Headsets)",
    "Cuidados Pessoais e Saúde (Barbeadores Elétricos, Escovas Rotativas)",
    "Home Office e Produtividade (Monitores Ergonomicos, Suportes, Cadeiras)"
]

def gerar_artigo_groq():
    """Solicita à IA Groq (Llama 3) um artigo completo formatado em HTML."""
    nicho_escolhido = random.choice(NICHOS)
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Você é um redator profissional especializado em guias de compra e reviews de produtos para o mercado brasileiro.
    Escreva um artigo de blog altamente persuasivo, otimizado para SEO, focado na categoria: {nicho_escolhido}.

    DIRETRIZES OBRIGATÓRIAS:
    1. Crie um Título chamativo que desperte curiosidade de compra.
    2. Desenvolva o texto em HTML estruturado contendo <h2>, <h3>, <p>, <ul> e <li>.
    3. Inclua pelo menos 2 botões de CTA (Call to Action) em HTML com visual moderno destacando o link de afiliado.
       O link do botão DEVE SER EXATAMENTE: {AFFILIATE_LINK}
       Exemplo de botão HTML:
       <div style="text-align: center; margin: 30px 0;">
         <a href="{AFFILIATE_LINK}" target="_blank" rel="nofollow noopener" style="background-color: #FF9900; color: #111111; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 8px; display: inline-block; font-size: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">👉 VER MELHORES OFERTAS NA AMAZON</a>
       </div>

    Responda ESTRITAMENTE em formato JSON no seguinte modelo:
    {{
      "titulo": "Título do artigo aqui",
      "conteudo": "Conteúdo HTML aqui..."
    }}
    """

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "Você é um gerador de artigos no formato JSON estrito."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "response_format": {"type": "json_object"}
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    dados = response.json()
    resultado = json.loads(dados["choices"][0]["message"]["content"])
    return resultado["titulo"], resultado["conteudo"]


def publicar_no_blogger(titulo, conteudo):
    """Autentica na API do Blogger e publica o novo post."""
    creds = Credentials(
        token=None,
        refresh_token=GOOGLE_REFRESH_TOKEN,
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )

    service = build("blogger", "v3", credentials=creds)

    body = {
        "kind": "blogger#post",
        "title": titulo,
        "content": conteudo
    }

    post = service.posts().insert(blogId=BLOG_ID, body=body).execute()
    return post.get("url")


if __name__ == "__main__":
    print("🚀 Iniciando execução do Robô Afiliado...")
    try:
        print("✍️ Gerando artigo persuasivo na Groq...")
        titulo, conteudo = gerar_artigo_groq()
        print(f"📌 Título gerado: {titulo}")

        print(f"📤 Publicando no blog (ID: {BLOG_ID})...")
        url_post = publicar_no_blogger(titulo, conteudo)

        print(f"✅ SUCESSO! Artigo publicado em: {url_post}")

    except Exception as erro:
        print(f"❌ Ocorreu um erro na execução: {erro}")
        raise erro

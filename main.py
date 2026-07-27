import os
import json
import random
from google import genai
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ==========================================
# CONFIGURAÇÕES DE MERCADOS E AFILIADOS
# ==========================================
BLOGGER_API_VERSION = "v3"
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Mapeamento de Mercados: País -> Idioma -> Link do País -> Subnichos
MERCADOS = [
    {
        "pais": "Brasil",
        "idioma": "Português",
        "moeda": "R$",
        "affiliate_tag": os.getenv("AFFILIATE_TAG_BR", "https://seu-link-afiliado-br.com"),
        "subnichos": [
            "Fones de Ouvido Bluetooth",
            "Smartwatches para Treino",
            "Aspiradores de Pó Robô",
            "Air Fryers Sem Óleo"
        ]
    },
    {
        "pais": "Estados Unidos",
        "idioma": "Inglês",
        "moeda": "$",
        "affiliate_tag": os.getenv("AFFILIATE_TAG_US", "https://seu-link-afiliado-us.com"),
        "subnichos": [
            "Wireless Bluetooth Earbuds",
            "Fitness Smartwatches",
            "Robot Vacuum Cleaners",
            "Air Fryers"
        ]
    },
    {
        "pais": "Espanha",
        "idioma": "Espanhol",
        "moeda": "€",
        "affiliate_tag": os.getenv("AFFILIATE_TAG_ES", "https://seu-link-afiliado-es.com"),
        "subnichos": [
            "Auriculares Inalámbricos Bluetooth",
            "Relojes Inteligentes Deportivos",
            "Aspiradores Robot",
            "Freidoras sin Aceite"
        ]
    }
]


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


def gerar_conteudo_gemini(mercado, subnicho):
    """Gera um artigo no idioma e moeda corretos do país selecionado."""
    client = genai.Client(api_key=GEMINI_API_KEY)

    prompt = f"""
    Você é um redator profissional de SEO e Copywriting focado em marketing de afiliados.
    Escreva um artigo persuasivo e altamente otimizado sobre o subnicho '{subnicho}'.

    CONTEXTO DO MERCADO:
    - País Alvo: {mercado['pais']}
    - Idioma OBRIGATÓRIO do Artigo: {mercado['idioma']}
    - Símbolo da Moeda Local: {mercado['moeda']}

    Regras OBRIGATÓRIAS:
    1. Retorne a resposta estritamente no formato JSON com as chaves: "titulo" e "conteudo_html".
    2. O artigo deve ser escrito inteiramente no idioma {mercado['idioma']}.
    3. Use HTML nativo simples para o Blogger (<h3>, <p>, <ul>, <li>, <strong>).
    4. NÃO inclua <html>, <head>, <body> ou ```html.
    5. Insira a seguinte chamada para ação (CTA) formatada exatamente com este link:
       <p style="text-align: center; margin: 25px 0;"><a href="{mercado['affiliate_tag']}" target="_blank" rel="nofollow" style="background-color: #28a745; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">👉 Check Best Deals & Updated Prices</a></p>
       (Adapte o texto do botão acima para o idioma {mercado['idioma']}).
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
    if not all([CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, GEMINI_API_KEY]):
        print("Erro: Variáveis de ambiente essenciais não foram configuradas.")
        return

    # 1. Escolhe o país/mercado primeiro
    mercado_selecionado = random.choice(MERCADOS)
    # 2. Escolhe um subnicho adequado para o idioma do país
    subnicho_selecionado = random.choice(mercado_selecionado["subnichos"])

    print(f"🌍 País Selecionado: {mercado_selecionado['pais']} ({mercado_selecionado['idioma']})")
    print(f"📦 Subnicho: {subnicho_selecionado}")
    print(f"🔗 Link de Afiliado Utilizado: {mercado_selecionado['affiliate_tag']}")

    try:
        service = get_blogger_service()
        blogs = service.blogs().listByUser(userId="self").execute()
        
        if not blogs.get("items"):
            print("Erro: Nenhum blog encontrado.")
            return

        blog_id = blogs["items"][0]["id"]

        print("Gerando artigo com IA...")
        titulo, conteudo_html = gerar_conteudo_gemini(mercado_selecionado, subnicho_selecionado)

        body = {
            "title": titulo,
            "content": conteudo_html
        }

        print("Publicando no Blogger...")
        post = service.posts().insert(blogId=blog_id, body=body).execute()
        print(f"🚀 Artigo publicado com sucesso no idioma {mercado_selecionado['idioma']}: {post.get('url')}")

    except Exception as e:
        print(f"❌ Erro na execução: {e}")


if __name__ == "__main__":
    executar_robo()

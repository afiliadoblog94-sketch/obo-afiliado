import os
import json
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# ==========================================
# CONFIGURAÇÕES DA OPERAÇÃO MATRIZ
# ==========================================
BLOGGER_API_VERSION = "v3"
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG", "seu-link-afiliado-aqui")

def get_blogger_service():
    """Autentica e retorna o serviço da API do Blogger usando o Refresh Token."""
    credentials = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build("blogger", BLOGGER_API_VERSION, credentials=credentials)

def gerar_conteudo_funil(subnicho, pais):
    """Gera a estrutura editorial focada em SEO: Long-tail | Dor/Desejo | Nome do Blog."""
    titulo = f"Melhores opções de {subnicho} para comprar online em {pais}"
    
    conteudo = f"""
    <p>Se você está procurando por <strong>{subnicho}</strong> de alta qualidade, selecionamos as melhores opções com excelente custo-benefício disponíveis no mercado internacional para {pais}.</p>
    
    <h3>Por que escolher este modelo?</h3>
    <p>A escolha correta garante durabilidade, eficiência e economia a longo prazo. Avaliamos os principais pontos de dor e desejo dos consumidores antes de recomendar.</p>
    
    <p>👉 <a href="{AFFILIATE_TAG}" target="_blank" rel="nofollow"><strong>Clique aqui para verificar o preço atualizado e garantir o seu com desconto!</strong></a></p>
    """
    return titulo, conteudo

def criar_e_publicar_artigo():
    service = get_blogger_service()
    
    # Exemplo de parâmetros operacionais globais
    pais = "Brasil"
    subnicho = "Eletrônicos e Utilidades"
    blog_nome = "Meu Blog Afiliado"
    
    # 1. Criação do Blog via API (caso necessário) ou uso do blog principal
    # Nota: A API gerencia posts e páginas. A criação inicial do blog pode ser listada/validada.
    try:
        blogs = service.blogs().listByUser(userId="self").execute()
        if not blogs.get("items"):
            print("Nenhum blog encontrado na conta matriz.")
            return
        
        blog_id = blogs["items"][0]["id"]
        print(f"Blog conectado com sucesso: {blogs['items'][0]['name']} (ID: {blog_id})")
        
        # 2. Geração do Artigo Editorial
        titulo, conteudo = gerar_conteudo_funil(subnicho, pais)
        
        body = {
            "title": titulo,
            "content": conteudo
        }
        
        # 3. Publicação Automatizada
        post = service.posts().insert(blogId=blog_id, body=body).execute()
        print(f"Sucesso! Artigo publicado: {post.get('url')}")
        
    except Exception as e:
        print(f"Erro durante a execução da operação: {e}")

if __name__ == "__main__":
    print("Iniciando ciclo de operação do robô...")
    criar_e_publicar_artigo()

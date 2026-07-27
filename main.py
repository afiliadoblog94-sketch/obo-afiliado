import os
import csv
import random
import subprocess
import requests
from datetime import datetime
from groq import Groq

def executar_git_push():
    """Faz o commit e o push automático do arquivo CSV atualizado para o GitHub."""
    print("Realizando commit e push automático do arquivo CSV...")
    try:
        subprocess.run(["git", "config", "--global", "user.name", "github-actions[bot]"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
        subprocess.run(["git", "add", "artigos_afiliados_global.csv"], check=True)
        
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "m", "🤖 [Bot 100% Automático] Blog criado e artigo publicado"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Arquivo CSV global enviado com sucesso para o GitHub!")
        else:
            print("Nenhuma alteração detectada para commit.")
    except Exception as e:
        print(f"AVISO: Não foi possível fazer o push automático: {e}")

def obter_token_acesso():
    """Gera um token de acesso válido usando o OAuth 2.0 do Google."""
    refresh_token = os.environ.get("GOOGLE_REFRESH_TOKEN")
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    if not refresh_token or not client_id or not client_secret:
        return None

    try:
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token"
        }
        resp = requests.post(token_url, data=payload)
        return resp.json().get("access_token")
    except Exception as e:
        print(f"Erro ao obter token de acesso: {e}")
        return None

def criar_blog_no_blogger(nome_blog, idioma):
    """Cria o blog automaticamente no Blogger via API e retorna o Blog ID."""
    print(f"Criando o blog '{nome_blog}' automaticamente no Blogger...")
    access_token = obter_token_acesso()
    if not access_token:
        print("Token de acesso não disponível para criar o blog.")
        return None

    try:
        url = "https://www.googleapis.com/blogger/v3/users/self/blogs"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "name": nome_blog,
            "locale": {"language": idioma}
        }
        
        resp = requests.post(url, headers=headers, json=body)
        if resp.status_code == 200:
            dados_blog = resp.json()
            blog_id = dados_blog.get("id")
            print(f"Blog criado com sucesso! ID: {blog_id}")
            return blog_id
        else:
            print(f"Erro ao criar blog no Blogger: {resp.text}")
            return None
    except Exception as e:
        print(f"Erro na requisição de criação do blog: {e}")
        return None

def publicar_no_blogger(titulo, conteudo, blog_id):
    """Envia o artigo gerado diretamente para o Blogger via API."""
    print(f"Publicando o artigo no Blogger (Blog ID: {blog_id})...")
    access_token = obter_token_acesso()
    if not access_token:
        return False

    try:
        post_url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "title": titulo,
            "content": conteudo
        }
        
        resp_post = requests.post(post_url, headers=headers, json=body)
        if resp_post.status_code == 200:
            print("Artigo publicado com sucesso no Blogger!")
            return True
        else:
            print(f"Erro ao publicar no Blogger: {resp_post.text}")
            return False
    except Exception as e:
        print(f"Erro na comunicação com a API do Blogger: {e}")
        return False

def executar_robo_global():
    print("Iniciando o Ciclo 100% Automatizado (Global / Múltiplos Países)...")
    
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("ERRO: GROQ_API_KEY não configurada nos Secrets do GitHub.")

    # Matriz Global (O robô gerencia tudo dinamicamente)
    paises_alvo = [
        {"pais": "Brasil", "idioma": "pt-BR", "marketplace": "Amazon Brasil / Mercado Livre"},
        {"pais": "França", "idioma": "fr", "marketplace": "Amazon.fr"},
        {"pais": "Espanha", "idioma": "es", "marketplace": "Amazon.es"},
        {"pais": "Estados Unidos", "idioma": "en", "marketplace": "Amazon.com"},
        {"pais": "Alemanha", "idioma": "de", "marketplace": "Amazon.de"},
        {"pais": "Itália", "idioma": "it", "marketplace": "Amazon.it"},
        {"pais": "Reino Unido", "idioma": "en", "marketplace": "Amazon.co.uk"},
        {"pais": "México", "idioma": "es", "marketplace": "Amazon.com.mx"},
        {"pais": "Canadá", "idioma": "en", "marketplace": "Amazon.ca"},
        {"pais": "Japão", "idioma": "ja", "marketplace": "Amazon.co.jp"}
    ]

    alvo_selecionado = random.choice(paises_alvo)
    pais = alvo_selecionado["pais"]
    idioma = alvo_selecionado["idioma"]
    marketplace = alvo_selecionado["marketplace"]

    print(f"País Selecionado: {pais} | Idioma: {idioma} | Marketplace: {marketplace}")

    try:
        client = Groq(api_key=groq_api_key)
        
        # 1. IA define o subnicho e a identidade do blog autonomamente
        print(f"IA gerando identidade comercial para o mercado de {pais}...")
        prompt_identidade = (
            f"Atue como um Estrategista Chefe de Marketing Digital e SEO focado no mercado da {pais}. "
            f"Selecione de forma autônoma 1 subnicho altamente lucrativo utilizando o {marketplace}. "
            "Crie um nome comercial atraente, curto e sem caracteres especiais para um blog. "
            "Responda estritamente no seguinte formato de texto simples:\n"
            "SUBNICHO: [Nome do Subnicho]\n"
            "NOME_BLOG: [Nome Criativo para o Blog]\n"
            "TEMA_ARTIGO: [Título long-tail de alta conversão para o primeiro artigo]"
        )
        
        resposta_id = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_identidade}]
        )
        
        dados_criacao = resposta_id.choices[0].message.content
        print(f"\n--- Estratégia Definida ---\n{dados_criacao}\n-----------------------------")

        # Extrai os dados gerados pela IA
        nome_blog = "Afiliado Global"
        titulo_artigo = "Artigo Exclusivo"
        for linha in dados_criacao.split('\n'):
            if "NOME_BLOG:" in linha:
                nome_blog = linha.replace("NOME_BLOG:", "").strip()
            if "TEMA_ARTIGO:" in linha:
                titulo_artigo = linha.replace("TEMA_ARTIGO:", "").strip()

        # 2. Criação automática do Blog no Blogger via API (Zero cliques manuais)
        blog_id = criar_blog_no_blogger(nome_blog, idioma)

        # 3. Geração do Artigo Otimizado em Funil
        print("Gerando o artigo estruturado com links de afiliados...")
        prompt_sistema = (
            f"Você é um redator sênior de SEO, especialista em copywriting para conversão em e-commerce ({marketplace})."
        )
        prompt_usuario = (
            f"Com base nestes dados:\n{dados_criacao}\n\n"
            "Crie um artigo completo estruturado com:\n"
            "1. Título otimizado.\n"
            "2. Introdução focada em resolver uma dor/desejo.\n"
            "3. Corpo detalhado com recomendações de produtos do {marketplace}.\n"
            "4. Chamada para Ação (CTA) estratégica para os links de afiliado."
        )
        
        resposta_artigo = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        
        conteudo_gerado = resposta_artigo.choices[0].message.content
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 4. Publicação Automática no Blog recém-criado
        status_pub = "Gerado no CSV"
        if blog_id:
            if publicar_no_blogger(titulo_artigo, conteudo_gerado, blog_id):
                status_pub = f"Blog Criado e Post Publicado (ID: {blog_id})"

        # 5. Salvamento no CSV e Backup no GitHub
        nome_arquivo = "artigos_afiliados_global.csv"
        arquivo_existe = os.path.exists(nome_arquivo)
        
        with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if not arquivo_existe:
                escritor.writerow(["Data/Hora", "País / Idioma", "Estratégia e Subnicho", "Conteúdo", "Status"])
            escritor.writerow([data_atual, f"{pais} ({idioma})", dados_criacao, conteudo_gerado, status_pub])
            
        executar_git_push()
        print("Ciclo 100% automatizado concluído com sucesso!")

    except Exception as e:
        print(f"Erro crítico no fluxo automatizado: {e}")
        raise e

if __name__ == "__main__":
    executar_robo_global()

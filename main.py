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
            subprocess.run(["git", "commit", "-m", "🤖 [Bot Master Global] Sincronização e postagem automatizada"], check=True)
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

def registrar_na_planilha_mestra(data_hora, pais, subnicho, nome_blog, status):
    """Registra as métricas e o status da postagem na Planilha Mestra do Google Sheets (se configurado)."""
    sheet_id = os.environ.get("GOOGLE_SHEET_ID")
    if not sheet_id:
        print("GOOGLE_SHEET_ID não configurado. Salvamento centralizado via CSV ativo.")
        return

    access_token = obter_token_acesso()
    if not access_token:
        return

    try:
        url = f"https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/A1:append?valueInputOption=USER_ENTERED"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        body = {
            "values": [[data_hora, pais, subnicho, nome_blog, status]]
        }
        requests.post(url, headers=headers, json=body)
        print("Dados sincronizados com a Planilha Mestra no Google Sheets!")
    except Exception as e:
        print(f"Erro ao registrar na planilha mestra: {e}")

def executar_robo_global():
    print("Iniciando o Ciclo Mestre de Expansão Global e Conversão...")
    
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("ERRO: GROQ_API_KEY não configurada nos Secrets do GitHub.")

    paises_alvo = [
        {"pais": "Brasil", "idioma": "pt-BR", "marketplace": "Amazon Brasil / Mercado Livre", "fuso": "America/Sao_Paulo"},
        {"pais": "França", "idioma": "fr", "marketplace": "Amazon.fr", "fuso": "Europe/Paris"},
        {"pais": "Espanha", "idioma": "es", "marketplace": "Amazon.es", "fuso": "Europe/Madrid"},
        {"pais": "Estados Unidos", "idioma": "en", "marketplace": "Amazon.com", "fuso": "America/New_York"},
        {"pais": "Alemanha", "idioma": "de", "marketplace": "Amazon.de", "fuso": "Europe/Berlin"},
        {"pais": "Itália", "idioma": "it", "marketplace": "Amazon.it", "fuso": "Europe/Rome"},
        {"pais": "Reino Unido", "idioma": "en", "marketplace": "Amazon.co.uk", "fuso": "Europe/London"},
        {"pais": "México", "idioma": "es", "marketplace": "Amazon.com.mx", "fuso": "America/Mexico_City"},
        {"pais": "Canadá", "idioma": "en", "marketplace": "Amazon.ca", "fuso": "America/Toronto"},
        {"pais": "Japão", "idioma": "ja", "marketplace": "Amazon.co.jp", "fuso": "Asia/Tokyo"}
    ]

    alvo_selecionado = random.choice(paises_alvo)
    pais = alvo_selecionado["pais"]
    idioma = alvo_selecionado["idioma"]
    marketplace = alvo_selecionado["marketplace"]

    print(f"País Selecionado: {pais} | Idioma: {idioma} | Marketplace: {marketplace}")

    try:
        client = Groq(api_key=groq_api_key)
        
        # 1. Inteligência da IA (Subnicho, Cadência, Horário de Pico e SEO)
        print(f"IA calculando a melhor estratégia de indexação e conversão para {pais}...")
        prompt_identidade = (
            f"Atue como um Especialista Sênior em SEO Técnico e Algoritmos de Indexação do Google. "
            f"Para o mercado da {pais} usando o marketplace {marketplace}:\n"
            "1. Selecione um subnicho altamente lucrativo.\n"
            "2. Defina a cadência ideal de postagem.\n"
            "3. Determine o melhor horário local de pico.\n"
            "4. Crie um nome comercial limpo para o blog e um título long-tail otimizado para SEO.\n"
            "Responda estritamente no seguinte formato:\n"
            "SUBNICHO: [Nome do Subnicho]\n"
            "CADENCIA_IDEAL: [Ex: 1 postagem a cada 24 horas]\n"
            "MELHOR_HORARIO: [Ex: 19:00]\n"
            "NOME_BLOG: [Nome Criativo para o Blog]\n"
            "TEMA_ARTIGO: [Título otimizado]"
        )
        
        resposta_id = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_identidade}]
        )
        
        dados_criacao = resposta_id.choices[0].message.content
        print(f"\n--- Estratégia Definida ---\n{dados_criacao}\n-----------------------------")

        subnicho_val = "Geral"
        nome_blog = "Global Market"
        titulo_artigo = "Artigo Exclusivo"
        for linha in dados_criacao.split('\n'):
            if "SUBNICHO:" in linha:
                subnicho_val = linha.replace("SUBNICHO:", "").strip()
            if "NOME_BLOG:" in linha:
                nome_blog = linha.replace("NOME_BLOG:", "").strip()
            if "TEMA_ARTIGO:" in linha:
                titulo_artigo = linha.replace("TEMA_ARTIGO:", "").strip()

        # 2. Criação Automática do Blog via API
        blog_id = criar_blog_no_blogger(nome_blog, idioma)

        # 3. Geração Editorial Alinhada às Diretrizes do Google (E-E-A-T)
        print("Gerando o artigo otimizado com foco em alta conversão e indexação...")
        prompt_sistema = (
            f"Você é um redator sênior de SEO e conformidade com as diretrizes de qualidade do Google (Helpful Content). "
            f"Escreva conteúdos originais, profundos, estruturados com tags HTML limpas (h2, h3, p, ul, li), focados em resolver a intenção de busca do usuário de {pais} e recomendar produtos do {marketplace}."
        )
        
        prompt_usuario = (
            f"Com base nestes dados estratégicos:\n{dados_criacao}\n\n"
            f"Escreva um artigo completo em {idioma} contendo introdução, subtópicos detalhados (H2/H3), recomendações de produtos do {marketplace} e uma Chamada para Ação (CTA) persuasiva. Retorne em HTML básico."
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

        # 4. Publicação Automática
        status_pub = "Gerado no CSV"
        if blog_id:
            if publicar_no_blogger(titulo_artigo, conteudo_gerado, blog_id):
                status_pub = f"Blog Criado e Post Publicado (ID: {blog_id})"

        # 5. Salvamento no CSV Local e Planilha Mestra
        nome_arquivo = "artigos_afiliados_global.csv"
        arquivo_existe = os.path.exists(nome_arquivo)
        
        with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if not arquivo_existe:
                escritor.writerow(["Data/Hora", "País / Idioma", "Estratégia e Horário", "Conteúdo", "Status"])
            escritor.writerow([data_atual, f"{pais} ({idioma})", dados_criacao, conteudo_gerado, status_pub])
            
        registrar_na_planilha_mestra(data_atual, pais, subnicho_val, nome_blog, status_pub)
        executar_git_push()
        
        print("Ciclo mestre concluído com sucesso absoluto!")

    except Exception as e:
        print(f"Erro crítico no fluxo mestre: {e}")
        raise e

if __name__ == "__main__":
    executar_robo_global()

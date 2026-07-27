import os
import csv
import random
import subprocess
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
            subprocess.run(["git", "commit", "-m", "🤖 [Bot Global] Novo artigo gerado para a matriz internacional"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Arquivo CSV global enviado com sucesso para o GitHub!")
        else:
            print("Nenhuma alteração detectada para commit.")
    except Exception as e:
        print(f"AVISO: Não foi possível fazer o push automático: {e}")

def executar_robo_global():
    print("Iniciando o Ciclo Global de Inteligência e Conteúdo (10 Países / 10 Subnichos)...")
    
    # 1. Validação da Chave da Groq
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("ERRO: GROQ_API_KEY não configurada nos Secrets do GitHub.")

    # 2. Matriz Global de Países, Idiomas e Marketplaces Locais
    paises_alvo = [
        {"pais": "Brasil", "idioma": "Português", "marketplace": "Amazon Brasil / Mercado Livre"},
        {"pais": "França", "idioma": "Francês", "marketplace": "Amazon.fr"},
        {"pais": "Espanha", "idioma": "Espanhol", "marketplace": "Amazon.es"},
        {"pais": "Estados Unidos", "idioma": "Inglês", "marketplace": "Amazon.com"},
        {"pais": "Alemanha", "idioma": "Alemão", "marketplace": "Amazon.de"},
        {"pais": "Itália", "idioma": "Italiano", "marketplace": "Amazon.it"},
        {"pais": "Reino Unido", "idioma": "Inglês", "marketplace": "Amazon.co.uk"},
        {"pais": "México", "idioma": "Espanhol", "marketplace": "Amazon.com.mx"},
        {"pais": "Canadá", "idioma": "Inglês/Francês", "marketplace": "Amazon.ca"},
        {"pais": "Japão", "idioma": "Japonês", "marketplace": "Amazon.co.jp"}
    ]

    # Escolhe aleatoriamente ou em ciclo um país da matriz global
    alvo_selecionado = random.choice(paises_alvo)
    pais = alvo_selecionado["pais"]
    idioma = alvo_selecionado["idioma"]
    marketplace = alvo_selecionado["marketplace"]

    print(f"País Selecionado: {pais} | Idioma: {idioma} | Marketplace: {marketplace}")

    try:
        client = Groq(api_key=groq_api_key)
        
        # 3. Fase 1: Autonomia na Escolha do Subnicho e Identidade Localizada
        print(f"IA analisando o mercado de {pais} e escolhendo o subnicho mais lucrativo...")
        prompt_identidade = (
            f"Atue como um Estrategista Chefe de Marketing Digital e SEO focado no mercado da {pais} (idioma: {idioma}). "
            f"Selecione de forma autônoma 1 subnicho altamente lucrativo para afiliados utilizando o {marketplace}. "
            "Crie um nome comercial atraente para o blog local e defina a linha editorial. "
            "Responda estritamente no seguinte formato de texto simples:\n"
            "SUBNICHO: [Nome do Subnicho]\n"
            "NOME_BLOG: [Nome Criativo para o Blog no idioma local]\n"
            "TEMA_ARTIGO: [Um título long-tail altamente pesquisado e de alta conversão para este artigo no idioma local]"
        )
        
        resposta_id = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_identidade}]
        )
        
        dados_criacao = resposta_id.choices[0].message.content
        print(f"\n--- Identidade e Estratégia ({pais}) ---\n{dados_criacao}\n---------------------------------------------")

        # 4. Fase 2: Construção Editorial em Funil no Idioma Nativo do País
        print(f"Gerando o artigo otimizado em {idioma} para {pais}...")
        prompt_sistema = (
            f"Você é um redator sênior de SEO nativo em {idioma}, especialista em copywriting para conversão em e-commerce ({marketplace}). "
            f"Escreva artigos detalhados, persuasivos e culturalmente adaptados para o público de {pais}."
        )
        
        prompt_usuario = (
            f"Com base nestes dados estratégicos gerados:\n{dados_criacao}\n\n"
            f"Crie um artigo completo para blog em {idioma} estruturado estritamente com:\n"
            "1. Um título longo (long-tail) otimizado para SEO local.\n"
            "2. Introdução focada em prender a atenção e resolver uma dor/desejo imediata do público local.\n"
            "3. Corpo do artigo detalhado, dividido em tópicos acionáveis, recomendando categorias de produtos do {marketplace}.\n"
            "4. Uma Chamada para Ação (CTA) estratégica direcionando o leitor para as ofertas do {marketplace}.\n"
            "Mantenha uma linguagem natural, profissional e altamente engajadora."
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

        # 5. Salvando os dados estruturados no arquivo CSV global
        nome_arquivo = "artigos_afiliados_global.csv"
        arquivo_existe = os.path.exists(nome_arquivo)
        
        print(f"Salvando dados no arquivo '{nome_arquivo}'...")
        with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if not arquivo_existe:
                escritor.writerow(["Data/Hora", "País / Idioma", "Estratégia e Subnicho", "Conteúdo do Artigo", "Status"])
            
            escritor.writerow([data_atual, f"{pais} ({idioma})", dados_criacao, conteudo_gerado, "Gerado Globalmente"])
            
        print("Dados gravados com sucesso no CSV global local!")

        # 6. Executa o envio automático para o GitHub
        executar_git_push()

        print("Ciclo global executado com sucesso absoluto!")

    except Exception as e:
        print(f"Erro crítico no fluxo global: {e}")
        raise e

if __name__ == "__main__":
    executar_robo_global()

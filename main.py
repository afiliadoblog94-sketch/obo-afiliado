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
        subprocess.run(["git", "add", "artigos_afiliados.csv"], check=True)
        
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", "🤖 [Bot] Autonomia Total: Novo nicho, identidade e artigo gerado"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Arquivo CSV enviado com sucesso para o GitHub!")
        else:
            print("Nenhuma alteração detectada para commit.")
    except Exception as e:
        print(f"AVISO: Não foi possível fazer o push automático: {e}")

def executar_robo_autonomo():
    print("Iniciando o Ciclo Autônomo de Inteligência e Conteúdo (Brasil)...")
    
    # 1. Validação da Chave da Groq
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("ERRO: GROQ_API_KEY não configurada nos Secrets do GitHub.")

    try:
        client = Groq(api_key=groq_api_key)
        
        # 2. Fase 1: Autonomia na Escolha do Subnicho e Identidade do Blog
        print("IA analisando o mercado brasileiro e escolhendo o subnicho mais lucrativo...")
        prompt_identidade = (
            "Atue como um Estrategista Chefe de Marketing Digital e SEO para o mercado do Brasil. "
            "Selecione de forma autônoma 1 subnicho altamente lucrativo para afiliados (focado em produtos da Amazon Brasil e Mercado Livre). "
            "Crie também um nome comercial atraente para o blog e defina a linha editorial. "
            "Responda estritamente no seguinte formato de texto simples:\n"
            "SUBNICHO: [Nome do Subnicho]\n"
            "NOME_BLOG: [Nome Criativo para o Blog]\n"
            "TEMA_ARTIGO: [Um título long-tail altamente pesquisado e de alta conversão para este artigo]"
        )
        
        resposta_id = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt_identidade}]
        )
        
        dados_criacao = resposta_id.choices[0].message.content
        print(f"\n--- Identidade e Estratégia Definidas pela IA ---\n{dados_criacao}\n------------------------------------------------")

        # 3. Fase 2: Construção Editorial em Funil e Otimização para E-commerce Brasil
        print("Gerando o artigo estruturado (Funil de Vendas + SEO + Chamada para Ação de Afiliado)...")
        prompt_sistema = (
            "Você é um redator sênior de SEO, especialista em copywriting para conversão em e-commerce (Amazon Brasil e Mercado Livre). "
            "Escreva artigos detalhados, persuasivos, focados na dor/desejo do público brasileiro."
        )
        prompt_usuario = (
            fCom base nestes dados estratégicos gerados:\n{dados_criacao}\n\n"
            "Crie um artigo completo para blog estruturado estritamente com:\n"
            "1. Um título longo (long-tail) otimizado para SEO.\n"
            "2. Introdução focada em prender a atenção e resolver uma dor/desejo imediata.\n"
            "3. Corpo do artigo detalhado, dividido em tópicos acionáveis, indicando implicitamente categorias de produtos encontrados na Amazon e no Mercado Livre.\n"
            "4. Uma Chamada para Ação (CTA) estratégica direcionando o leitor para as melhores ofertas do mercado.\n"
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

        # 4. Salvando os dados estruturados no arquivo CSV
        nome_arquivo = "artigos_afiliados.csv"
        arquivo_existe = os.path.exists(nome_arquivo)
        
        print(f"Salvando dados no arquivo '{nome_arquivo}'...")
        with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if not arquivo_existe:
                escritor.writerow(["Data/Hora", "Estratégia e Subnicho", "Conteúdo do Artigo", "Status"])
            
            escritor.writerow([data_atual, dados_criacao, conteudo_gerado, "Gerado Autonomamente"])
            
        print("Dados gravados com sucesso no CSV local!")

        # 5. Executa o envio automático para o GitHub
        executar_git_push()

        print("Ciclo autônomo executado com sucesso absoluto!")

    except Exception as e:
        print(f"Erro crítico no fluxo autônomo: {e}")
        raise e

if __name__ == "__main__":
    executar_robo_autonomo()

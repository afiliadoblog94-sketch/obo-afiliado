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
            subprocess.run(["git", "commit", "-m", "🤖 [Bot] Atualização automática de artigos de afiliados"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Arquivo CSV enviado com sucesso para o GitHub!")
        else:
            print("Nenhuma alteração detectada para commit.")
    except Exception as e:
        print(f"AVISO: Não foi possível fazer o push automático: {e}")

def executar_robo_afiliado():
    print("Iniciando o Ciclo de Conteúdo para Afiliados...")
    
    # 1. Validação da Chave da Groq
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("ERRO: GROQ_API_KEY não configurada nos Secrets do GitHub.")

    # 2. Temas focados estritamente na estratégia de afiliados
    temas_afiliados = [
        "Como começar no marketing de afiliados sem investimento inicial",
        "As melhores estratégias de tráfego orgânico para vender como afiliado",
        "Como escolher produtos de alta conversão para o seu nicho",
        "Erros comuns que afiliados iniciantes cometem e como evitar",
        "Como usar o marketing de conteúdo para gerar comissões diárias",
        "O guia definitivo para escalar suas vendas como afiliado digital"
    ]
    
    tema_escolhido = random.choice(temas_afiliados)
    print(f"Tema de afiliados selecionado: {tema_escolhido}")

    try:
        # 3. Geração de Conteúdo via Groq focada em Afiliados
        client = Groq(api_key=groq_api_key)
        print("Gerando artigo otimizado para conversão de afiliados...")
        
        prompt_sistema = "Você é um especialista em marketing de afiliados, SEO e copywriting de alta conversão."
        prompt_usuario = (
            f"Com base no tema '{tema_escolhido}', crie um artigo completo para blog estruturado estritamente com:\n"
            "1. Um título chamativo no formato long-tail otimizado para SEO.\n"
            "2. Uma introdução persuasiva focada em quebrar objeções e despertar o desejo do leitor.\n"
            "3. O corpo do artigo dividido em tópicos acionáveis com dicas práticas.\n"
            "4. Uma chamada para ação (CTA) estratégica direcionando o leitor para o link de afiliado.\n"
            "Mantenha um tom profissional, altamente engajador e focado em vendas."
        )
        
        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ]
        )
        
        conteudo_gerado = resposta.choices[0].message.content
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("\n--- Artigo de Afiliados Gerado ---")
        print(conteudo_gerado)
        print("-----------------------------------")

        # 4. Salvando os dados no arquivo CSV específico de afiliados
        nome_arquivo = "artigos_afiliados.csv"
        arquivo_existe = os.path.exists(nome_arquivo)
        
        print(f"Salvando dados no arquivo '{nome_arquivo}'...")
        with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            if not arquivo_existe:
                escritor.writerow(["Data/Hora", "Tema de Afiliados", "Conteúdo do Artigo", "Status"])
            
            escritor.writerow([data_atual, tema_escolhido, conteudo_gerado, "Pronto para o Blog"])
            
        print("Dados gravados com sucesso no CSV local!")

        # 5. Executa o envio automático para o GitHub
        executar_git_push()

        print("Ciclo de afiliados executado com sucesso absoluto!")

    except Exception as e:
        print(f"Erro crítico no fluxo: {e}")
        raise e

if __name__ == "__main__":
    executar_robo_afiliado()

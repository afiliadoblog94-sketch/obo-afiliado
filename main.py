import os
import csv
from datetime import datetime
from groq import Groq

def executar_robo_afiliado():
    print("Iniciando o Ciclo Automatizado do Robô Afiliado...")
    
    # 1. Validação da Chave da Groq
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("ERRO: GROQ_API_KEY não configurada nos Secrets do GitHub.")

    try:
        # 2. Geração de Conteúdo via Groq
        client = Groq(api_key=groq_api_key)
        print("Gerando artigo otimizado para conversão...")
        
        prompt_sistema = "Você é um especialista em SEO internacional e marketing de afiliados."
        prompt_usuario = (
            "Crie um título de artigo seguindo estritamente a fórmula: "
            "[Termo de pesquisa long-tail] | [Dor ou Desejo do usuário] | [Forma & Cacau Global] "
            "e escreva o parágrafo inicial de introdução focado em conversão de afiliados."
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
        
        print("\n--- Conteúdo Gerado para o Blog ---")
        print(conteudo_gerado)
        print("------------------------------------")

        # 3. Salvando os dados localmente no arquivo CSV
        nome_arquivo = "artigos_gerados.csv"
        arquivo_existe = os.path.exists(nome_arquivo)
        
        print(f"Salvando dados no arquivo '{nome_arquivo}'...")
        with open(nome_arquivo, mode="a", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            # Se o arquivo for novo, escrevemos o cabeçalho
            if not arquivo_existe:
                escritor.writerow(["Data/Hora", "Conteúdo Gerado", "Status"])
            
            escritor.writerow([data_atual, conteudo_gerado, "Pendente Publicação"])
            
        print("Dados gravados com sucesso no arquivo CSV!")
        print("Ciclo executado com sucesso absoluto!")

    except Exception as e:
        print(f"Erro crítico no fluxo: {e}")
        raise e

if __name__ == "__main__":
    executar_robo_afiliado()

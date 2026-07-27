import os
from groq import Groq
from datetime import datetime
import gspread
from google.oauth2.credentials import Credentials

def executar_robo_afiliado():
    print("Iniciando o Ciclo Automatizado do Robô Afiliado...")
    
    # 1. Validação de Segredos
    groq_api_key = os.environ.get("GROQ_API_KEY")
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    if not groq_api_key:
        raise ValueError("ERRO: GROQ_API_KEY não configurada.")
    if not client_id or not client_secret:
        raise ValueError("ERRO: Credenciais do Google OAuth não configuradas nos segredos.")

    try:
        # 2. Geração de Conteúdo via Groq (Padrão Long-Tail | Dor/Desejo | Nome do Blog)
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

        # 3. Conexão e Gravação na Planilha Afiliado via OAuth
        # Nota: Certifique-se de autorizar o token ou utilizar o fluxo de salvamento do gspread
        print("Preparando registro na planilha...")
        # (Opcional nesta fase inicial de testes, garantindo que o fluxo principal está integro)

        print("Ciclo executado com sucesso absoluto!")

    except Exception as e:
        print(f"Erro crítico no fluxo: {e}")
        raise e

if __name__ == "__main__":
    executar_robo_afiliado()

import os
from groq import Groq

def testar_robo_com_sheets():
    print("Iniciando o Robô Afiliado com Groq e Google Sheets...")
    
    # 1. Validando chave da Groq
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("ERRO: A chave GROQ_API_KEY não foi encontrada nos segredos do GitHub.")

    # 2. Validando credenciais do Google Client
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    if client_id and client_secret:
        print("Credenciais do Google Client ID e Secret carregadas com sucesso.")
    else:
        print("Aviso: Credenciais do Google Client não totalmente preenchidas.")

    try:
        # 3. Gerando conteúdo de tecnologia com a Groq
        client = Groq(api_key=groq_api_key)
        print("Gerando pauta e artigo de tecnologia via Groq...")
        
        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Você é um especialista em marketing de afiliados."},
                {"role": "user", "content": "Crie uma sugestão de título de artigo focado em placa de vídeo custo-benefício e um resumo curto de 1 linha."}
            ]
        )
        
        conteudo_gerado = resposta.choices[0].message.content
        
        print("\n--- Conteúdo Gerado pela IA ---")
        print(conteudo_gerado)
        print---------------------------------")
        
        # 4. Estrutura pronta para salvar no Google Sheets
        print("Estrutura pronta para registrar os dados na planilha do Google Sheets.")
        print("Robô executado com sucesso absoluto!")
        
    except Exception as e:
        print(f"Erro crítico durante a execução: {e}")
        raise e

if __name__ == "__main__":
    testar_robo_com_sheets()

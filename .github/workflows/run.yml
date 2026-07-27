import os
import json
import gspread
from google.oauth2.service_account import Credentials
from groq import Groq

def testar_robo_com_sheets():
    print("Iniciando o Robô Afiliado com Groq e Google Sheets...")
    
    # 1. Validando chave da Groq
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("ERRO: A chave GROQ_API_KEY não foi encontrada nos segredos do GitHub.")

    # 2. Validando credenciais do Google Sheets (Service Account JSON)
    google_creds_json = os.environ.get("GCP_SERVICE_ACCOUNT_JSON")
    if not google_creds_json:
        raise ValueError("ERRO: O segredo GCP_SERVICE_ACCOUNT_JSON não foi encontrado.")

    try:
        # Configurando a autenticação do Google Sheets via Conta de Serviço
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        creds_dict = json.loads(google_creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        gc = gspread.authorize(creds)
        
        print("Autenticação com o Google Sheets realizada com sucesso via Conta de Serviço.")

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
        print("---------------------------------")
        
        # 4. Exemplo de como abrir a planilha e salvar os dados (substitua 'NomeDaSuaPlanilha' pelo nome exato do seu arquivo)
        # 
        # planilha = gc.open("NomeDaSuaPlanilha")
        # aba = planilha.sheet1
        # aba.append_row([conteudo_gerado, "Pendente"])
        # print("Dados salvos na planilha com sucesso!")

        print("Robô executado com sucesso absoluto!")
        
    except Exception as e:
        print(f"Erro crítico durante a execução: {e}")
        raise e

if __name__ == "__main__":
    testar_robo_com_sheets()

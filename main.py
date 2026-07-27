import os
import json
import gspread
from google.oauth2.service_account import Credentials
from groq import Groq
from datetime import datetime

def executar_robo_afiliado():
    print("Iniciando o Ciclo Automatizado do Robô Afiliado...")
    
    # 1. Validação de Segredos
    groq_api_key = os.environ.get("GROQ_API_KEY")
    google_creds_json = os.environ.get("GCP_SERVICE_ACCOUNT_JSON")
    
    if not groq_api_key:
        raise ValueError("ERRO: GROQ_API_KEY não configurada.")
    if not google_creds_json:
        raise ValueError("ERRO: GCP_SERVICE_ACCOUNT_JSON não configurada.")

    try:
        # 2. Conexão com Google Sheets
        scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        creds_dict = json.loads(google_creds_json)
        creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
        gc = gspread.authorize(creds)
        print("Conexão com Google Sheets estabelecida com sucesso.")

        # 3. Geração de Conteúdo via Groq (Padrão Long-Tail | Dor/Desejo | Nome do Blog)
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

        # 4. Salvando dados na Planilha Mestra "Planilha Afiliado"
        try:
            planilha = gc.open("Planilha Afiliado")
            aba = planilha.sheet1
            aba.append_row([data_atual, conteudo_gerado, "Publicado - Topo de Funil", "Pendente Indexação"])
            print("Dados registrados na planilha 'Planilha Afiliado' com sucesso!")
        except Exception as sheet_err:
            print(f"AVISO: Não foi possível gravar na planilha: {sheet_err}")

        print("Ciclo executado com sucesso absoluto!")

    except Exception as e:
        print(f"Erro crítico no fluxo: {e}")
        raise e

if __name__ == "__main__":
    executar_robo_afiliado()

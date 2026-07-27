import os
from google import genai

def testar_robo():
    print("Iniciando o Robô Afiliado...")
    
    # Validando se a chave secreta do Gemini existe no ambiente do GitHub
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("ERRO: A chave GEMINI_API_KEY não foi encontrada nos segredos do GitHub.")

    # Validando se as credenciais do Google Client estão presentes para futuras automações
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    if client_id and client_secret:
        print("Credenciais do Google Client ID e Secret carregadas com sucesso.")
    else:
        print("Aviso: Credenciais do Google Client opcionais não totalmente preenchidas.")

    try:
        # Inicializando o cliente oficial do Google GenAI
        client = genai.Client(api_key=api_key)
        
        print("Conectando ao modelo Gemini para gerar conteúdo de tecnologia...")
        resposta = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Escreva uma introdução curta, otimizada para SEO e persuasiva para um artigo de tecnologia sobre placas de vídeo custo-benefício.",
        )
        
        print("\n--- Teste de Geração com Gemini ---")
        print(resposta.text)
        print("-----------------------------------")
        print("Robô conectado, testado e funcionando com sucesso absoluto!")
        
    except Exception as e:
        print(f"Erro crítico ao comunicar com a API do Gemini: {e}")
        raise e

if __name__ == "__main__":
    testar_robo()

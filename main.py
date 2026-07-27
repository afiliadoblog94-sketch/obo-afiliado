import os
from openai import OpenAI

def testar_robo():
    print("Iniciando o Robô Afiliado com ChatGPT...")
    
    # Validando se a chave secreta da OpenAI existe no ambiente do GitHub
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("ERRO: A chave OPENAI_API_KEY não foi encontrada nos segredos do GitHub.")

    # Validando se as credenciais do Google Client continuam disponíveis
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    
    if client_id and client_secret:
        print("Credenciais do Google Client ID e Secret carregadas com sucesso.")
    else:
        print("Aviso: Credenciais do Google Client opcionais não totalmente preenchidas.")

    try:
        # Inicializando o cliente oficial da OpenAI
        client = OpenAI(api_key=api_key)
        
        print("Conectando ao modelo GPT para gerar conteúdo de tecnologia...")
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um especialista em marketing de afiliados e tecnologia."},
                {"role": "user", "content": "Escreva uma introdução curta, otimizada para SEO e persuasiva para um artigo de tecnologia sobre placas de vídeo custo-benefício."}
            ]
        )
        
        texto_gerado = resposta.choices[0].message.content
        
        print("\n--- Teste de Geração com ChatGPT ---")
        print(texto_gerado)
        print("-------------------------------------")
        print("Robô conectado, testado e funcionando com sucesso absoluto via OpenAI!")
        
    except Exception as e:
        print(f"Erro crítico ao comunicar com a API da OpenAI: {e}")
        raise e

if __name__ == "__main__":
    testar_robo()

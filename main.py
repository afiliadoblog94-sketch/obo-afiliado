import os
from google import genai

# Configurando a API do Gemini com o segredo salvo no GitHub
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada nos segredos do GitHub.")

client = genai.Client(api_key=api_key)

def testar_robo():
    print("Iniciando o Robô Afiliado...")
    resposta = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="Escreva uma introdução curta e persuasiva para um artigo de tecnologia sobre placas de vídeo.",
    )
    print("\n--- Teste de Geração com Gemini ---")
    print(resposta.text)
    print("-----------------------------------")
    print("Robô conectado e funcionando com sucesso!")

if __name__ == "__main__":
    testar_robo()

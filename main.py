import os
import time
from google import genai
from google.genai.errors import ClientError

def testar_robo():
    print("Iniciando o Robô Afiliado...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("ERRO: A chave GEMINI_API_KEY não foi encontrada nos segredos do GitHub.")

    client = genai.Client(api_key=api_key)
    
    max_tentativas = 3
    tentativa = 1

    while tentativa <= max_tentativas:
        try:
            print(f"Tentativa {tentativa} de conexão com o Gemini...")
            resposta = client.models.generate_content(
                model="gemini-2.0-flash",
                contents="Escreva uma introdução curta, otimizada para SEO e persuasiva para um artigo de tecnologia sobre placas de vídeo custo-benefício.",
            )
            
            print("\n--- Teste de Geração com Gemini ---")
            print(resposta.text)
            print("-----------------------------------")
            print("Robô conectado, testado e funcionando com sucesso absoluto!")
            return
            
        except ClientError as e:
            if e.code == 429:
                print(f"Limite da API atingido (Erro 429). Aguardando 30 segundos antes de tentar novamente... (Tentativa {tentativa}/{max_tentativas})")
                time.sleep(30)
                tentativa += 1
            else:
                print(f"Erro da API do Gemini: {e}")
                raise e
        except Exception as e:
            print(f"Erro crítico inesperado: {e}")
            raise e

    raise Exception("Falha após várias tentativas devido ao limite de cota da API (Erro 429).")

if __name__ == "__main__":
    testar_robo()

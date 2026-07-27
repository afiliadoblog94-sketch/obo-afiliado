# 1. IA analisa o mercado, define o subnicho, a cadência ideal e o melhor horário SEO
        print(f"IA calculando a cadência ideal de indexação e horário de pico para {pais}...")
        prompt_identidade = (
            f"Atue como um Especialista Sênior em SEO Técnico e Algoritmos de Indexação do Google (Googlebot). "
            f"Para o mercado da {pais} usando o marketplace {marketplace}:\n"
            "1. Selecione um subnicho altamente lucrativo.\n"
            "2. Defina a cadência ideal de postagem (ex: 1 artigo por dia, a cada 2 dias) para garantir que o Googlebot indexe o conteúdo sem penalizar por spam de volume.\n"
            "3. Determine o MELHOR HORÁRIO do dia (no fuso local) para a postagem.\n"
            "4. Crie um nome comercial limpo para o blog e um título long-tail otimizado para SEO.\n"
            "Responda estritamente no seguinte formato:\n"
            "SUBNICHO: [Nome do Subnicho]\n"
            "CADENCIA_IDEAL: [Ex: 1 postagem a cada 24 horas para retenção de autoridade]\n"
            "MELHOR_HORARIO: [Ex: 08:00 da manhã - Horário de indexação matinal]\n"
            "NOME_BLOG: [Nome Criativo para o Blog]\n"
            "TEMA_ARTIGO: [Título otimizado]"
        )

import requests
import json

# Defina a chave da API
api_key = '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'

# URL base para a API da Groq
base_url = "https://api.groq.ai/v1/semantic-analysis"  # exemplo de endpoint, confira a documentação da Groq


# Função para enviar o texto para a análise semântica da Groq
def analyze_text_with_groq(text):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Corpo da requisição com o texto a ser analisado
    payload = {
        "text": text,
        "analysis_type": "extract_entities"  # ou o tipo de análise necessário, dependendo da Groq
    }

    response = requests.post(base_url, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return response.json()  # Retorna a resposta JSON contendo as entidades extraídas
    else:
        print(f"Erro ao enviar a requisição: {response.status_code}")
        return None


# Função para processar os resultados e extrair informações chave
def process_extracted_data(data):
    # Extração semântica: Como exemplo, identificamos campos como nome, quantidade, valor, etc.
    extracted_info = {
        'produtos': []
    }

    for item in data['entities']:  # 'entities' depende do formato da resposta da API
        produto = {}

        # Aqui você pode customizar conforme os campos da resposta da API
        if 'nome_produto' in item:
            produto['nome'] = item['nome_produto']
        if 'quantidade' in item:
            produto['quantidade'] = item['quantidade']
        if 'valor' in item:
            produto['valor'] = item['valor']
        if 'tipo_produto' in item:
            produto['tipo'] = item['tipo_produto']
        if 'marca' in item:
            produto['marca'] = item['marca']
        if 'volume' in item:
            produto['volume'] = item['volume']

        extracted_info['produtos'].append(produto)

    return extracted_info


# Exemplo de texto a ser analisado
texto = """
0,00 736,56 0,00 0,00 0,00 6421 0,00 0,00 0,00 0,00 736,56 40,9200 18,00 CX  6 BEBIDA LACTEA
CAROLINA
1,25KG EMB TAM
F ACAI/MOR109721
EANs: 7896691104706
"""

# Enviar o texto para a análise semântica
result = analyze_text_with_groq(texto)

# Verificar e processar os resultados
if result:
    produtos = process_extracted_data(result)
    print("Produtos extraídos:", json.dumps(produtos, indent=2))
else:
    print("Não foi possível processar os dados.")


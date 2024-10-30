import os
import re
from PyPDF2 import PdfReader, PdfWriter
from groq import Groq

# Caminho para as pastas
folder = 'C:\\Users\\ryane\\OneDrive\\Área de Trabalho\\NF`s'

# Lista de códigos específicos a serem pesquisados
codigos_especificos = ['42795', '31716', '31717', '31719', '31721', '43200', '43199', '54670', '31712']

# Inicializa o cliente da Groq com a chave da API
client = Groq(api_key=os.environ.get(""))

# Função para fazer a requisição à IA da Groq
def fazer_requisicao(texto):
    messages = [
        {"role": "user", "content": texto}
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

# Função para extrair informações específicas do PDF
def extrair_informacoes(caminho_pdf):
    global data_emissao
    leitor = PdfReader(caminho_pdf)
    writer_pdf = PdfWriter()
    respostas = []

    for i, pagina in enumerate(leitor.pages):
        texto = pagina.extract_text()

        if any(codigo in texto for codigo in codigos_especificos):
            writer_pdf.add_page(pagina)

            # Fazer requisição à IA da Groq
            instrucoes = (
                "Você irá ler esse pdf e identificar a data de emissão,e deve retornar como resposta a apenas a data "
            )
            texto_completo = f"{instrucoes}\n\n{texto}"
            resposta = fazer_requisicao(texto_completo)
            respostas.append(resposta)

    # Salvar todas as páginas em um único arquivo PDF
    if len(writer_pdf.pages) > 0:
        # Extraindo a data de emissão da primeira resposta
        data_emissao = extrair_data_emissao(respostas[0])  # Apenas a primeira, pode ser adaptado para múltiplas
        data_emissao_formatada = data_emissao.replace('/', '-')  # Substituir / por -
        nome_pdf_final = os.path.join(folder, f'STOK NF_{data_emissao_formatada}.pdf')
        with open(nome_pdf_final, 'wb') as novo_pdf:
            writer_pdf.write(novo_pdf)
        print(f'Todas as páginas salvas como {nome_pdf_final}')

# Função para extrair a data de emissão a partir da resposta
def extrair_data_emissao(resposta):
    # Exemplo de regex para capturar a data no formato DD/MM/YYYY ou similar
    match = re.search(r'\d{2}/\d{2}/\d{4}', resposta)
    return match.group(0) if match else 'data_desconhecida'

# Processar todos os arquivos PDF na pasta de origem
for arquivo in os.listdir(folder):
    if arquivo.endswith('.pdf'):
        caminho_pdf = os.path.join(folder, arquivo)
        extrair_informacoes(caminho_pdf)

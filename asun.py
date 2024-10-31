import os
import re
from PyPDF2 import PdfReader, PdfWriter

# Caminho para as pastas
folder = 'C:\\Users\\ryane\\OneDrive\\Área de Trabalho\\NF`s'

# Lista de códigos específicos a serem pesquisados
codigos_especificos = [
    '34405', '34407', '34408', '34411', '34458', '34478', '34479',
    '34481', '34482', '34492', '34496', '34497', '34498', '34499',
    '34500', '34501', '34502', '34503', '34505', '34506', '34507',
    '34508', '34510', '34512', '34513', '35475', '46828', '35975'
]
# Função para extrair a data de emissão do texto
def extrair_data_emissao(texto):
    # Regex para encontrar a data antes de "Data da emissão"
    match = re.search(r'RS\s*(\d{2}-\d{2}-\d{4})', texto)
    return match.group(1) if match else 'data_desconhecida'

# Função para gerar um nome de arquivo único
def gerar_nome_unico(nome_base):
    indice = 1
    nome = nome_base
    while os.path.exists(nome):
        nome = f"{nome_base}({indice})"
        indice += 1
    return nome

# Função para extrair informações específicas do PDF
def extrair_informacoes(caminho_pdf):
    leitor = PdfReader(caminho_pdf)
    writer_pdf = PdfWriter()
    data_emissao = 'data_desconhecida'

    for i, pagina in enumerate(leitor.pages):
        texto = pagina.extract_text()
        if any(codigos in texto for codigos in codigos_especificos):
            writer_pdf.add_page(pagina)
            # Tenta extrair a data de emissão do texto
            data_extraida = extrair_data_emissao(texto)
            if data_extraida != 'data_desconhecida':
                data_emissao = data_extraida

    # Salvar todas as páginas em um único arquivo PDF
    if len(writer_pdf.pages) > 0:
        nome_pdf_base = os.path.join(folder, f'ASUN NF_{data_emissao}.pdf')
        nome_pdf_final = gerar_nome_unico(nome_pdf_base)
        with open(nome_pdf_final, 'wb') as novo_pdf:
            writer_pdf.write(novo_pdf)
        print(f'Todas as páginas salvas como {nome_pdf_final}')

# Processar todos os arquivos PDF na pasta de origem
for arquivo in os.listdir(folder):
    if arquivo.endswith('.pdf'):
        caminho_pdf = os.path.join(folder, arquivo)
        extrair_informacoes(caminho_pdf)

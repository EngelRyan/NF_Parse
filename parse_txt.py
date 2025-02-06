import os
import re
import requests
from io import BytesIO
from PyPDF2 import PdfMerger

# Caminho da pasta onde os arquivos estão
folder = 'C:\\Users\\Windows 10 Pro\\OneDrive\\Área de Trabalho\\NFS'

# Dicionário de clientes e seus respectivos mercados
clientes_mercado = {
    # Mercados ASUN
    '34405': 'ASUN CACHOEIRINHA CENTRO',
    '34407': 'ASUN CAVALHADA',
    '34408': 'ASUN RESTINGA',
    '34458': 'ASUN ESTANCIA',
    '34478': 'ASUN ALVORADA',
    '34479': 'ASUN MONTENEGRO',
    '34481': 'ASUN CANOAS',
    '34492': 'ASUN DOIS IRMAOS',
    '34496': 'ASUN ELDORADO DO SUL',
    '34497': 'ASUN SANTANA',
    '34498': 'ASUN PLINIO',
    '34499': 'ASUN IGARA',
    '34500': 'ASUN JUCA BATISTA',
    '34501': 'ASUN AZENHA',
    '34502': 'ASUN CONCEICAO',
    '34503': 'ASUN FLORIANOPOLIS',
    '34505': 'ASUN CANOAS NITEROI',
    '34507': 'ASUN REPUBLICA',
    '34510': 'ASUN GUAIBA',
    '34512': 'ASUN RITTER',
    '34513': 'ASUN CACHOEINHA VERANOPOLIS',
    '35475': 'ASUN GRAVATAÍ',
    '46828': 'ASUN PONTAL',
    # Mercados FORT
    '45999': 'RS-FORT ATACAD 345 CAX DO SUL',
    '41868': 'RS-FORT ATACAD 370 VIAMAO',
    '41869': 'RS-FORT ATACAD 545 CANOAS',
    '55660': 'RS-FORT ATACAD 885 ST CRUZ SUL',
    # Mercados STOK
    '42795': 'COMERCIAL ZAFFARI 10',
    '31717': 'COMERCIAL ZAFFARI 23',
    '31721': 'COMERCIAL ZAFFARI 35',
    '31716': 'COMERCIAL ZAFFARI 22',
    '43200': 'COMERCIAL ZAFFARI 39',
    '31719': 'COMERCIAL ZAFFARI 26',
    '43199': 'COMERCIAL ZAFFARI 42',
    '31712': 'COMERCIAL ZAFFARI 85',
    '54670': 'COMERCIAL ZAFFARI 51',
    # Mercados ATACADO, BIG e WAL MART
    '37400': 'ATACADÃO PORTO ALEGRE SERTORIO',
    '37401': 'ATACADÃO GRAVATAI',
    '37514': 'ATACADÃO PELOTAS',
    '37410': 'ATACADÃO PORTO ALEGRE VITOR VALPIRO',
    '31497': 'BIG CACHOEIRINHA',
    '31536': 'BIG GRAVATAI',
    '37416': 'WAL MART PORTO ALEGRE ASSIS BRASIL',
}

# Categorias de mercados
categorias = {
    "ASUN": [],
    "FORT": [],
    "STOK": [],
    "ATACADO_BIG_WALMART": [],
}

def extrair_dados(mensagem):

    numero_nota_regex = r"Nota Fiscal: (\d+)"
    valor_regex = r"Valor: ([\d,\.]+)"
    cliente_regex = r"Cliente: (\d{5}-[A-Z]+)"
    link_regex = r"Link da nota: (https?://[^\s]+\.pdf)"
    numero_nota = re.search(numero_nota_regex, mensagem)
    valor = re.search(valor_regex, mensagem)
    cliente = re.search(cliente_regex, mensagem)
    link = re.search(link_regex, mensagem)

    return {
        "numero_nota": numero_nota.group(1) if numero_nota else "Não encontrado",
        "valor": valor.group(1) if valor else "Não encontrado",
        "cliente": cliente.group(1) if cliente else "Não encontrado",
        "link": link.group(1) if link else "Não encontrado"
    }

def processar_arquivo(txt_path):

    with open(txt_path, 'r', encoding='utf-8') as file:
        texto = file.read()

    mensagens = texto.split('\n\n')

    for mensagem in mensagens:
        dados = extrair_dados(mensagem)

        numero_cliente = dados['cliente'].split('-')[0]
        nome_mercado = clientes_mercado.get(numero_cliente, "Mercado desconhecido")

        if numero_cliente in clientes_mercado:
            if "ASUN" in nome_mercado:
                categorias["ASUN"].append(mensagem)
            elif "FORT" in nome_mercado or "FORTE" in nome_mercado:
                categorias["FORT"].append(mensagem)
            elif "STOCK" in nome_mercado or "ZAFFARI" in nome_mercado:
                categorias["STOK"].append(mensagem)
            elif "ATACADÃO" in nome_mercado or "BIG" in nome_mercado or "WAL MART" in nome_mercado:
                categorias["ATACADO_BIG_WALMART"].append(mensagem)

def salvar_em_arquivos():
    for categoria, mensagens in categorias.items():
        if mensagens:
            output_file = os.path.join(folder, f"{categoria}_NF_.txt")
            with open(output_file, 'w', encoding='utf-8') as file:
                for mensagem in mensagens:
                    file.write(mensagem + '\n\n')
            print(f"Arquivo {categoria}_NF_.txt criado com sucesso em {output_file}")


def extrair_links_do_arquivo(txt_path):
    links = []
    with open(txt_path, 'r', encoding='utf-8') as file:
        texto = file.read()

    link_regex = r"https?://[^\s]+"
    links = re.findall(link_regex, texto)

    # Remover links que terminam com .xml
    links = [link for link in links if not link.endswith('.xml')]

    return links

def baixar_nota(link):
    try:
        response = requests.get(link)
        response.raise_for_status()

        return BytesIO(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a nota de {link}: {e}")
        return None

def baixar_e_juntar_notas(categoria):
    txt_path = os.path.join(folder, f"{categoria}_NF_.txt")

    if os.path.exists(txt_path):
        print(f"Iniciando o download das notas de {categoria}...")

        links = extrair_links_do_arquivo(txt_path)

        if not links:
            print(f"Não há links de notas no arquivo {txt_path}.")
            return

        pdf_merger = PdfMerger()

        for link in links:
            pdf_arquivo = baixar_nota(link)
            if pdf_arquivo:
                pdf_merger.append(pdf_arquivo)

        arquivo_final = os.path.join(folder, f"{categoria}.pdf")
        pdf_merger.write(arquivo_final)
        pdf_merger.close()

        print(f"Arquivo final gerado com sucesso: {arquivo_final}")
    else:
        print(f"Arquivo {txt_path} não encontrado!")

def baixar_todas_as_notas():
    categorias = ["ASUN", "FORT", "STOK", "ATACADO_BIG_WALMART"]

    for categoria in categorias:
        baixar_e_juntar_notas(categoria)

if __name__ == "__main__":
    txt_path = os.path.join(folder, "NOTAS.txt")

    processar_arquivo(txt_path)
    salvar_em_arquivos()
    baixar_todas_as_notas()

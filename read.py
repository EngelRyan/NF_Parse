import PyPDF2


# Função para ler o conteúdo do PDF
def ler_pdf(caminho_pdf):
    try:
        with open(caminho_pdf, 'rb') as arquivo_pdf:
            leitor = PyPDF2.PdfReader(arquivo_pdf)
            texto = ""

            # Itera pelas páginas do PDF
            for pagina in leitor.pages:
                texto += pagina.extract_text()

            return texto
    except Exception as e:
        print(f"Erro ao ler o PDF: {e}")
        return None


# Caminho do arquivo PDF
caminho = 'STOK PD_20-01-2025.pdf'

# Lê e exibe o conteúdo
texto_pdf = ler_pdf(caminho)

if texto_pdf:
    print(texto_pdf)

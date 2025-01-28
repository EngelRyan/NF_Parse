import PyPDF2
import os

# Função para ler o conteúdo de um PDF
def ler_pdf(caminho_pdf):
    try:
        with open(caminho_pdf, 'rb') as arquivo_pdf:
            leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
            texto = ""
            # Iterar por todas as páginas do PDF
            for pagina in leitor_pdf.pages:
                texto += pagina.extract_text()
            return texto
    except FileNotFoundError:
        return f"Erro: O arquivo {caminho_pdf} não foi encontrado."
    except Exception as e:
        return f"Erro ao ler o PDF: {e}"

# Caminho dos arquivos PDF no mesmo diretório do script
diretorio_atual = os.path.dirname(os.path.realpath(__file__))
pdf1 = os.path.join(diretorio_atual, "STOK PD_20-01-2025.pdf")
pdf2 = os.path.join(diretorio_atual, "STOK NF_22-01-2025.pdf")

# Ler os dois PDFs
texto_pdf1 = ler_pdf(pdf1)
texto_pdf2 = ler_pdf(pdf2)

# Exibir os textos dos PDFs (você pode fazer algo mais interessante com eles depois)
print("Conteúdo do PDF 1:")
print(texto_pdf1)

print("\nConteúdo do PDF 2:")
print(texto_pdf2)

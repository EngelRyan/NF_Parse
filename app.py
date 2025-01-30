from base import extract_first_occurrence, extract_all_occurrences
import os
from PyPDF2 import PdfReader, PdfWriter

def main():

    folder = 'C:\\Users\\Windows 10 Pro\\OneDrive\\Área de Trabalho\\NFS'

    # List of specific codes for STOK
    stok_codes = ['42795', '31716', '31717', '31719', '31721', '43200', '43199', '54670', '31712']

    # List of specific codes for FORT
    fort_codes = ['41867', '45999', '41868','55660']

    # List of specific codes for ASUN
    asun_codes = [
        '34405', '34407', '34408', '34411', '34458', '34478', '34479',
        '34481', '34482', '34492', '34496', '34497', '34498', '34499',
        '34500', '34501', '34502', '34503', '34505', '34506', '34507',
        '34508', '34510', '34512', '34513', '35475', '46828', '35975'
    ]

    atacadao_codes= ['37400','37401','37410','37514','31497','31536','37416']

   
    # Extract only the first occurrence for each category
    for file in os.listdir(folder):
        pdf_path = os.path.join(folder, file)
        extract_all_occurrences('STOK', stok_codes, pdf_path)
        extract_all_occurrences('FORT', fort_codes, pdf_path)
        extract_all_occurrences('ASUN', asun_codes, pdf_path)
        extract_all_occurrences('ATACADAO', atacadao_codes, pdf_path)

if __name__ == '__main__':
    main()

import os
import re
from PyPDF2 import PdfReader, PdfWriter

# Path to the folders
folder = 'C:\\Users\\Windows 10 Pro\\OneDrive\\Área de Trabalho\\NFS'

# Function to extract the issue date from the text
def extract_issue_date(text):

    match = re.search(r'RS\s*(\d{2}-\d{2}-\d{4})', text)

    return match.group(1) if match else 'unknown_date'

# Function to generate a unique filename
def generate_unique_name(base_name):

    index = 1
    name, extension = os.path.splitext(base_name)
    unique_name = name

    while os.path.exists(unique_name + extension):

        unique_name = f"{name}({index})"
        index += 1

    return unique_name + extension

# Function to save the pages to a PDF file
def save_pdf(writer, name, issue_date):

    if len(writer.pages) > 0:

        pdf_base_name = os.path.join(folder, f'{name} NF_{issue_date}.pdf')
        pdf_final_name = generate_unique_name(pdf_base_name)

        with open(pdf_final_name, 'wb') as new_pdf:
            writer.write(new_pdf)

        print(f'Pages saved as {pdf_final_name}')


# Function to extract only the first occurrence of specified codes from the PDF
def extract_first_occurrence(name, codes, pdf_path):

    if not pdf_path.lower().endswith('.pdf'):  # Check if it's a PDF
        print(f"Skipping {pdf_path} (not a PDF)")
        return

    reader = PdfReader(pdf_path)
    found_notes = set()  # Set to store already found codes

    for page in reader.pages:

        text = page.extract_text()
        match = re.search(r'(\d{1,3}(?:\.\d{3})*)\s*RECEBEMOS', text)
        print(match)

        # Check if any specific code is present on the page
        for code in codes:

            if code in text and match not in found_notes:
                print(found_notes)

                writer = PdfWriter()
                writer.add_page(page)
                found_notes.add(match)
                issue_date = extract_issue_date(text)

                save_pdf(writer, name, issue_date)

                break

    save_pdf(writer, name, issue_date)

# Function to extract all occurrences of specified codes from the PDF
def extract_all_occurrences(name, codes, pdf_path):

    if not pdf_path.lower().endswith('.pdf'):  # Check if it's a PDF
        print(f"Skipping {pdf_path} (not a PDF)")
        return

    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    issue_date = 'unknown_date'

    for page in reader.pages:
        text = page.extract_text()

        for code in codes:

            if code in text:

                writer.add_page(page)

                if issue_date == 'unknown_date':
                    issue_date = extract_issue_date(text)

    save_pdf(writer, name, issue_date)

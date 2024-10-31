# NF_Parse

NF_Parse é uma ferramenta desenvolvida para extrair informações relevantes de arquivos PDF de Notas Fiscais (NF) e facilitar a análise de vendas em mercados de grande rede. Este script utiliza a biblioteca PyPDF2 para leitura de PDFs e a API da Groq para análise de texto.

## Funcionalidades

- **Extração de Informações**: O script analisa PDFs em busca de códigos específicos e extrai informações relevantes, como a data de emissão.
- **Integração com IA**: Utiliza a IA da Groq para interpretar o texto extraído e fornecer dados de maneira estruturada.
- **Geração de PDFs**: Salva as páginas relevantes em um novo arquivo PDF, facilitando o compartilhamento e a organização das informações.

## Tecnologias Utilizadas

- [Python](https://www.python.org/) - Linguagem de programação
- [PyPDF2](https://pypdf2.readthedocs.io/en/latest/) - Biblioteca para manipulação de arquivos PDF
- [Groq](https://groq.com/) - API de processamento de linguagem natural

## Pré-requisitos

- Python 3.x
- Bibliotecas necessárias:
  ```bash
  pip install PyPDF2 groq

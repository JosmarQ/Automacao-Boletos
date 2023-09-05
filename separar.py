import PyPDF2
import os
from datetime import datetime

def separar_pdf():

    pasta_origem = 'boletos'
    nome_do_mes = datetime.now().strftime('%B')
    pasta_com_mes = os.path.join(pasta_origem, nome_do_mes)
    os.makedirs(pasta_com_mes, exist_ok=True)

    # Abrir o arquivo PDF
    with open('Boletos.pdf', 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Crie uma pasta para salvar as páginas individuais

        os.makedirs(pasta_com_mes, exist_ok=True)

        # Itere através de cada página do PDF
        for page_number in range(len(pdf_reader.pages)):
            # Crie um novo arquivo PDF para cada página
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(pdf_reader.pages[page_number])

            # Salve a página individual em um arquivo
            output_file = os.path.join(pasta_com_mes, f'page_{page_number + 1}.pdf')
            with open(output_file, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)

    print('Páginas separadas com sucesso!')


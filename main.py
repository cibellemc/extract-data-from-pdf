from datetime import date
import io
import re
import pdfplumber
import pandas as pd
from PyPDF2 import PdfReader

from flask import Flask, redirect, render_template, request, send_file, url_for

app = Flask(__name__)

@app.route("/")
def get_fatura():
    if request.method == "GET":
        return render_template ("index.html")

@app.route("/pdfconverter", methods=('GET', 'POST'))
def converter():
    pdf_file = request.files['fatura']
    #pdf_file = request.form.get['fatura']
    print(type(pdf_file))
    reader = PdfReader(pdf_file)

    # quantidade de páginas do documento
    numero_de_paginas = len(reader.pages)

    # listas para armazenar os dados
    data = []
    instalacoes = []
    valores = []
    index = -1

    # transformar pdf em txt
    with open("fatura.txt", "w", encoding='UTF-8') as output_file:
        for page_num in range(1, numero_de_paginas - 2):
            page = reader.pages[page_num]
            text = page.extract_text()
            #print(text)
            output_file.write(text)

    # extrair informações do arquivo txt
    with open('fatura.txt', 'r', encoding='UTF-8') as f:
        lines = f.readlines()

        for i in range(len(lines)):
            line = lines[i]

            if "Instalação" in line:
                info_instalacao = line.split()[1]
                instalacoes.append(info_instalacao)

            if "Valor:" in line:
                padrao = re.compile(r'Recolhimento:(.*?)Valor: (\d+\.\d+)', re.DOTALL)
                resultados = padrao.findall(line)

            # Imprima os resultados
                for resultado in resultados:
                    valores.append(resultado[1])
                    

    # função para extrair informações do arquivo PDF
    with pdfplumber.open(pdf_file) as pdf:
        for page_num in range(1, numero_de_paginas - 2):
            first_page = pdf.pages[page_num]
            text = first_page.extract_text()
            
            lines = text.split('\n')
            for line in lines:
                if "CAT" in line:
                    leitura_anterior = line.split()[4]
                    leitura_atual = line.split()[5]
                    medido = line.split()[6]
                    index = index + 1

                    # adiciona as informações à lista de dados
                    data.append({
                        'Instalação': int(instalacoes[index]),
                        'Leit.Anterior': leitura_anterior,
                        'Leit.Atual': leitura_atual,
                        'Medido': medido,
                        'Valor': valores[index]
                    })

    df = pd.DataFrame(data)

    data_atual = date.today().strftime("%Y-%m-%d") 
    nome_arquivo = 'fatura_' + str(data_atual) + '.xlsx'

    df.to_excel('static/' + nome_arquivo, index=None)

    return redirect(url_for('static', filename=nome_arquivo))

    #return render_template('download.html')

@app.route('/return-files/')
def return_files_tut():
    try:
        fatura = 'fatura_' + str(date.today().strftime("%Y-%m-%d") ) + '.xlsx'
        buf_str = io.StringIO(fatura)

        return send_file(io.BytesIO(buf_str.read().encode("utf-8")), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", download_name='fatura')
    except Exception as e:
        return str(e)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081,debug=True) 
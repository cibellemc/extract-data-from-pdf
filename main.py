from datetime import date
import re
import pdfplumber
import pandas as pd
from PyPDF2 import PdfReader

reader = PdfReader("fatura.pdf")

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
with pdfplumber.open("fatura.pdf") as pdf:
    for page_num in range(1, 5 - 2):
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
df.to_excel('fatura_' + str(data_atual) + '.xlsx', index=None)

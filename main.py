from PyPDF2 import PdfReader

reader = PdfReader("fatura.pdf")

# quantidade de páginas do documento
number_of_pages = len(reader.pages)

# função pra transformar em arquivo txt
with open("myfile.txt", "w") as output_file:
    for page_num in range(2, number_of_pages - 2):
        page = reader.pages[page_num]
        text = page.extract_text()
        output_file.write(text)

linhas_encontradas = []

# função pra printar a linha depois do cabeçalho de valor faturado e a instalação
with open('myfile.txt', 'r') as f:
    lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i]
        if "Instalação" in line:
            print(line.strip())
            linhas_encontradas.append(line.strip())

with open('linhas_encontradas.txt', 'w', encoding='UTF-8') as output_file:
    for linha in linhas_encontradas:
        output_file.write(f"{linha}\n")

"""        if "Descrição" in line:
            # Encontrou a linha, salva a próxima linha
            if i + 1 < len(lines):
                print(lines[i + 1].strip())
                # Faça o que quiser com a linha a seguir, por exemplo, salvar em um arquivo
                with open('linha_a_seguir.txt', 'w', encoding='UTF-8') as output_file:
                    output_file.write(linha_a_seguir)
"""


# função pra ver cada linha individual
"""Counter = 0
with open('myfile.txt', 'r') as f:
    Content = f.read() 
    CoList = Content.split("\n") 
    
    for i in CoList: 
        if i: 
            Counter += 1

    f.seek(0)  # Volta para o início do arquivo

    lines = f.readlines()

    for num, line in enumerate(lines, 1):    
        print(f"Linha {num} - {line.strip()}")
"""

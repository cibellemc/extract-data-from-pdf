from PyPDF2 import PdfReader

reader = PdfReader("fatura.pdf")

# quantidade de páginas do documento
number_of_pages = len(reader.pages)

# função pra transformar em arquivo txt
with open("myfile.txt", "w") as output_file:
    for page_num in range(1, 2):
        page = reader.pages[page_num]
        text = page.extract_text()
        output_file.write(text)

instalacoes = []
valores = []

# função pra printar a linha depois do cabeçalho de valor faturado e a instalação
with open('myfile.txt', 'r') as f:
    lines = f.readlines()

    for i in range(len(lines)):
        line = lines[i]

        if "Instalação" in line:
            info = line.split()[1]
            print(info)
            # print(line.strip())
            instalacoes.append(info)


        if "ValorCAT" in line:
            # Encontrou a linha, salva a próxima linha
            if i + 1 < len(lines):
                info = line.split()[7]
                info = line.split()[8]
                info = line.split()[9]
                # print(lines[i + 1].strip())
                valores.append(line.strip())


with open('instalacoes.txt', 'w', encoding='UTF-8') as output_file:
    for linha in instalacoes:
        output_file.write(f"{linha}\n")

with open('valores_faturados.txt', 'w', encoding='UTF-8') as output_file:
    for linha in valores:
        output_file.write(f"{linha}\n")

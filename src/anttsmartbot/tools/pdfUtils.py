import tabula
import pandas as pd


# Nome do arquivo PDF
pdf_file = '/home/fernando/Área de trabalho/viagens/viagens 19-01-2023/Arraial d\'Ajuda 20 a 26.pdf'

# Extraindo todas as tabelas do PDF em uma lista de DataFrames
dfs = tabula.read_pdf(pdf_file, pages='all', multiple_tables=True)

# Escrevendo cada DataFrame em uma planilha separada em um arquivo Excel
with pd.ExcelWriter('/home/fernando/Área de trabalho/viagens/viagens 19-01-2023/tabelakkk.xlsx') as writer:
    for i, df in enumerate(dfs):
        df.to_excel(writer)

print("Conversão concluída com sucesso!")
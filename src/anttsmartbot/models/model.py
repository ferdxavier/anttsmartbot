import pandas as pd

class Passageiro:
    id: str
    nome: str
    numero_doc: str
    tipo_doc: str
    orgao: str
    situacao: str
    crianca_colo: str
    telefone: str

class ListaViagem:
    cnpj: str
    senha: str
    site: str
    placa: str
    tipo_viagem: str
    num_solicitacao: str
    passageiros = []

SITUACAO = [
    # SITUACAO[0]
    "Brasileiro Maior",
    
    # SITUACAO[1]
    "Brasileiro Adolescente",
    
    # SITUACAO[2]
    "Brasileiro Criança",
    
    # SITUACAO[3]
    "Estrageiro"
]

TIPO_DOCUMENTO = {
        # Brasileiro Maior
        f'{SITUACAO[0]}': [
                "Carteira de Identidade",
                "Carteira Profissional",
                "Registro de Identificação Civil - RIC",
                "Carteira de Trabalho",
                "Passaporte Brasileiro",
                "Carteira Nacional de Habilitação - CNH",
                "Autorização de Viagem - FUNAI",
                "CPF" 
            ],
        # Brasileiro Adolescente
        f'{SITUACAO[1]}': [
                "Carteira de Identidade",
                "Carteira Profissional",
                "Registro de Identificação Civil - RIC",
                "Carteira de Trabalho",
                "Passaporte Brasileiro",
                "Carteira Nacional de Habilitação - CNH",
                "Autorização de Viagem - FUNAI",
                "CPF" 
            ],
        # Brasileiro Criança
        f'{SITUACAO[2]}': [
                "Passaporte Brasileiro",
                "Certidão Nascimento",
                "Carteira de Identidade",
                "Autorização de Viagem - FUNAI",
                "CPF"
            ], 
        # Estrageiro
        f'{SITUACAO[3]}': [
                "Passaporte Estrageiro",
                "Cédula de Identidade de Estrangeiro -CIE",
                "Identidade diplomática ou consular",
                "Outro documento legal de viagem"
        ] 
    }

TIPO_VIAGEM = [
    "NORMAL",
    "ATIPICA"
]
    
def load_traveler_List(str):
    try:
        dataframe = pd.read_excel(str)
        data = load_file(dataframe)
        
        if data["error"]:
            return {'error': data["error"], 'traveler_List': None} 
        
        return {'error': None, 'traveler_List': data["traveler_List"]}
    except FileNotFoundError:
        return {'error': f'Arquivo "{str}" não encontrado!', 'traveler_List': None}
    
def load_file(dataframe):
    lista = ListaViagem()
    lista.passageiros = []
    try:
        lista.placa = str(dataframe.iloc[0, 2]).strip()
        lista.tipo_viagem = str(dataframe.iloc[1, 2]).strip()
        if lista.tipo_viagem not in TIPO_VIAGEM:
            return {"error": "Verifique o tipo da viagem. (NORMAL OU ATIPICA)", "traveler_List": None}
        lista.num_solicitacao = str(dataframe.iloc[2, 2]).strip()
        return load_travelers(dataframe, lista)
    except IndexError:
        return {"error": "Verifique o cabeçalho do arquivo. (placa, Tipo da Viagem ou número da solicitação)", "traveler_List": None}
    
    
def load_travelers(dataframe, lista):
    rows = dataframe[6:]
    for r in range(0, len(rows)):
        passageiro = Passageiro()
        passageiro.id = rows.iloc[r, 0]
        passageiro.nome = str(rows.iloc[r, 1]).strip()
        passageiro.numero_doc = str(rows.iloc[r, 2])
        passageiro.tipo_doc = str(rows.iloc[r, 3]).strip()
        passageiro.orgao = str(rows.iloc[r, 4]).strip()
        passageiro.situacao = str(rows.iloc[r, 5]).strip()
        passageiro.crianca_colo = str(rows.iloc[r, 6]).strip()
        passageiro.telefone = str(rows.iloc[r, 7]).strip()
        result = isValidPassageiro(passageiro)
        if not result:
            lista.passageiros.append(passageiro)
        else:
            return {"error": f'Erro encontrado no passageiro número {r + 1}: {result}', "traveler_List": lista}
           
    num_lap_child = lap_child_count(lista.passageiros)
    if num_lap_child > (len(lista.passageiros) - num_lap_child):
        return {"error": f'Não é possível digitalizar a viajem. Existem mais crianças de COLO do que outros tipos de passageiros.', "traveler_List": lista}
    
    lista.passageiros = sort_list_by_situacao(lista.passageiros)
    
    return {"error": None, "traveler_List": lista}

def sort_list_by_situacao(passageiros):
    lap_childs = []
    adult = []
    for passageiro in passageiros:
        if str(passageiro.crianca_colo).upper() == "SIM":
            lap_childs.append(passageiro)
        else:
            adult.append(passageiro)
    
    adult.extend(lap_childs)
    return adult

def lap_child_count(passageiros):
    num = 0
    for passageiro in passageiros:
        if str(passageiro.crianca_colo).upper() == "SIM":
            num += 1
    return num       
    
def isValidPassageiro(passageiro: Passageiro):
    if len(passageiro.nome) < 3 or passageiro.nome == 'nan':
        return "Nome inválido."
    if len(passageiro.numero_doc) < 3 or passageiro.numero_doc == 'nan':
        return "Documento inválido."
    if len(passageiro.orgao) < 2 or passageiro.orgao == 'nan':
        return "Órgão é inválido."
    if not passageiro.situacao in SITUACAO:
        return f'A situação do passageiro é inválida. ({passageiro.situacao})'
    if not passageiro.tipo_doc in TIPO_DOCUMENTO[passageiro.situacao]:
        return f'O tipo de documento é inválido. ({passageiro.tipo_doc})'
    if str(passageiro.crianca_colo).upper() == "SIM" and str(passageiro.situacao).upper() != str(SITUACAO[2]).upper():
        return f'O campo SITUAÇÃO deve ser informado como "{SITUACAO[2]}" para Criança de Colo.'
    
    return None
"""
def load_traveler_List_PDF_normal(str):
    pdf_file = open(str, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    texto = ''
    for page in range(num_pages):
        
        page_obj = pdf_reader.pages[page]
        print(page_obj.extract_text())
        print()
        texto += page_obj.extract_text()
    pdf_file.close()
    
def load_traveler_List_PDF_dig(str):
    pass
"""

#load_traveler_List_PDF_normal('/home/fernando/listas/listateste2.pdf')
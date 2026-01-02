import pandas as pd
import unicodedata
import re

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
    "Brasileiro Maior",      # SITUACAO[0]
    "Brasileiro Adolescente",# SITUACAO[1]
    "Brasileiro Criança",    # SITUACAO[2]
    "Estrageiro"             # SITUACAO[3]
]

TIPO_DOCUMENTO = {
    f'{SITUACAO[0]}': [
        "Carteira de Identidade", "Carteira Profissional", "Registro de Identificação Civil - RIC",
        "Carteira de Trabalho", "Passaporte Brasileiro", "Carteira Nacional de Habilitação - CNH",
        "Autorização de Viagem - FUNAI", "CPF"
    ],
    f'{SITUACAO[1]}': [
        "Carteira de Identidade", "Carteira Profissional", "Registro de Identificação Civil - RIC",
        "Carteira de Trabalho", "Passaporte Brasileiro", "Carteira Nacional de Habilitação - CNH",
        "Autorização de Viagem - FUNAI", "CPF"
    ],
    f'{SITUACAO[2]}': [
        "Passaporte Brasileiro", "Certidão Nascimento", "Carteira de Identidade",
        "Autorização de Viagem - FUNAI", "CPF"
    ],
    f'{SITUACAO[3]}': [
        "Passaporte Estrageiro", "Cédula de Identidade de Estrangeiro -CIE",
        "Identidade diplomática ou consular", "Outro documento legal de viagem"
    ]
}

TIPO_VIAGEM = ["NORMAL", "ARTIGO37I"]

def remove_accents(text):
    """Remove acentos para fins de comparação lógica."""
    if not text or text == 'nan': return ""
    try:
        text = unicodedata.normalize('NFD', str(text))
        text = re.sub(r'[\u0300-\u036f]', '', text)
        return text.strip()
    except:
        return str(text)

def load_traveler_List(file_path):
    try:
        dataframe = pd.read_excel(file_path)
        data = load_file(dataframe)
        if data["error"]:
            return {'error': data["error"], 'traveler_List': None}
        return {'error': None, 'traveler_List': data["traveler_List"]}
    except FileNotFoundError:
        return {'error': f'Arquivo "{file_path}" não encontrado!', 'traveler_List': None}

def load_file(dataframe):
    lista = ListaViagem()
    lista.passageiros = []
    try:
        # Placa: Removemos tudo para padronizar
        placa_raw = str(dataframe.iloc[0, 2]).upper().replace("-", "").replace(" ", "").replace(".", "")
        lista.placa = remove_accents(placa_raw)
        
        # Tipo Viagem: Compara normalizado mas busca o original
        tipo_raw = str(dataframe.iloc[1, 2]).strip().upper()
        lista.tipo_viagem = None
        for tv in TIPO_VIAGEM:
            if remove_accents(tv).upper() == remove_accents(tipo_raw):
                lista.tipo_viagem = tv
                break
        
        if not lista.tipo_viagem:
            return {"error": "Tipo da viagem inválido. (NORMAL OU ARTIGO37I)", "traveler_List": None}
            
        lista.num_solicitacao = str(dataframe.iloc[2, 2]).strip()
        return load_travelers(dataframe, lista)
    except IndexError:
        return {"error": "Verifique o cabeçalho do arquivo.", "traveler_List": None}

def is_list_file(passageiros, p_add: Passageiro):
    key_add = remove_accents(p_add.nome + p_add.numero_doc + p_add.orgao).upper()
    for p in passageiros:
        key_list = remove_accents(p.nome + p.numero_doc + p.orgao).upper()
        if key_add == key_list:
            return p.id
    return None

def load_travelers(dataframe, lista):
    rows = dataframe[6:]
    for r in range(0, len(rows)):
        passageiro = Passageiro()
        passageiro.id = str(rows.iloc[r, 0])
        
        # Carregamos limpando apenas espaços, sem remover acentos ainda
        passageiro.nome = str(rows.iloc[r, 1]).strip()
        passageiro.numero_doc = str(rows.iloc[r, 2]).strip()
        passageiro.tipo_doc = str(rows.iloc[r, 3]).strip()
        passageiro.orgao = str(rows.iloc[r, 4]).strip()
        passageiro.situacao = str(rows.iloc[r, 5]).strip()
        passageiro.crianca_colo = str(rows.iloc[r, 6]).strip()
        passageiro.telefone = str(rows.iloc[r, 7]).strip()

        result = isValidPassageiro(passageiro)
        
        if result != 'discard':
            if not result:
                dup_id = is_list_file(lista.passageiros, passageiro)
                if not dup_id:
                    lista.passageiros.append(passageiro)
                else:
                    return {"error": f'Passageiros {dup_id} e {passageiro.id} duplicados: {passageiro.nome}', "traveler_List": lista}
            else:
                return {"error": f'Erro no passageiro {passageiro.id}: {result}', "traveler_List": lista}
            
    num_lap = lap_child_count(lista.passageiros)
    if num_lap > (len(lista.passageiros) - num_lap):
        return {"error": "Mais crianças de colo do que acompanhantes.", "traveler_List": lista}
    
    lista.passageiros = sort_list_by_situacao(lista.passageiros)
    return {"error": None, "traveler_List": lista}

def isValidPassageiro(p: Passageiro):
    if is_empty_line_except_id(p):
        return 'discard'
    
    # Validação do Nome (permanece com regra de tamanho)
    if len(p.nome) < 3 or p.nome == 'nan':
        return "Nome inválido."

    # --- AJUSTE: Permite "-" no Documento ---
    if p.numero_doc == 'nan' or (len(p.numero_doc) < 3 and p.numero_doc != "-"):
        return "Documento inválido."

    # --- AJUSTE: Permite "-" no Tipo de Doc e Órgão ---
    # 1. Validar e Corrigir Situação
    sit_input = remove_accents(p.situacao).upper()
    situacao_encontrada = None
    for s in SITUACAO:
        if remove_accents(s).upper() == sit_input:
            situacao_encontrada = s
            break
            
    if not situacao_encontrada:
        return f"Situação inválida: {p.situacao}"
    p.situacao = situacao_encontrada

    # 2. Validar e Corrigir Tipo de Documento
    # Se for "-", aceitamos sem buscar na lista TIPO_DOCUMENTO
    if p.tipo_doc == "-":
        p.tipo_doc = "-" 
    else:
        doc_input = remove_accents(p.tipo_doc).upper()
        docs_possiveis = TIPO_DOCUMENTO[p.situacao]
        doc_encontrado = None
        for d in docs_possiveis:
            if remove_accents(d).upper() == doc_input:
                doc_encontrado = d
                break
        
        if not doc_encontrado:
            return f"Documento {p.tipo_doc} inválido para {p.situacao}"
        p.tipo_doc = doc_encontrado

    # 3. Validação Criança de Colo
    if str(p.crianca_colo).upper() == "SIM":
        if p.situacao != SITUACAO[2]:
            return f'Para Criança de Colo, a situação deve ser "{SITUACAO[2]}"'
            
    return None
def sort_list_by_situacao(passageiros):
    lap = [p for p in passageiros if str(p.crianca_colo).upper() == "SIM"]
    not_lap = [p for p in passageiros if str(p.crianca_colo).upper() != "SIM"]
    return not_lap + lap

def lap_child_count(passageiros):
    return sum(1 for p in passageiros if str(p.crianca_colo).upper() == "SIM")

def check_line(value: str):
    return value == 'nan' or len(str(value).strip()) == 0

def is_empty_line_except_id(p: Passageiro):
    fields = [p.nome, p.numero_doc, p.tipo_doc, p.orgao, p.situacao, p.crianca_colo, p.telefone]
    return all(check_line(f) for f in fields)

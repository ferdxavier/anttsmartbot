from .models.model import ListaViagem
from .tools.constants import ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME
from  .bot import execute_list
from os.path import join
import json

def load_minimal_infor(placa: str, solicitacao: str):
    with open(join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME), encoding='utf-8') as my_json:
        json_data = json.load(my_json)
        traveler_list = ListaViagem()
        traveler_list.cnpj = json_data["company"]
        traveler_list.senha = json_data["password"]
        traveler_list.site = json_data["site"]
        traveler_list.placa = placa
        traveler_list.num_solicitacao = solicitacao
        return traveler_list
    return None


def describe_list(placa: str, solicitacao: str):
    traveler_list = load_minimal_infor(placa, solicitacao)
    if traveler_list:
        date = execute_list(traveler_list)
        print()
        print(f'   | Placa........: {traveler_list.placa}')
        print(f'   | Solicicacao..: {traveler_list.num_solicitacao}')
        print(f'   | {len(traveler_list.passageiros)} passageiro(s) encontrados.')
        print()
        if not date['error']:
            id = 1
            for traveler in traveler_list.passageiros:
                print(f' {id:3} {traveler.nome:40} {traveler.numero_doc:20} {traveler.orgao:10}')
                id += 1
        else:
            print(f'   * {date['error']}')
    else:
        print(f'   Ocorreu um erro ao abrir o arquivo "{join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME)}"')


def remove_list(placa: str, solicitacao: str):
    traveler_list = load_minimal_infor(placa, solicitacao)
    if traveler_list:
        print("Implementar esvaziar lista")
    else:
        print(f'Ocorreu um erro ao abrir o arquivo "{join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME)}"')
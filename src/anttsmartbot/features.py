from .models.model import ListaViagem
from .tools import util
from .tools.constants import ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME, JSON_PATH_WORKDIR
from .bot import execute_list, execute_remove, execute_find_manifest
from .spy import process_file
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
    traveler_list = load_minimal_infor(placa.upper(), solicitacao)
    if traveler_list:
        data = execute_list(traveler_list)
        print()
        print(f'   | Solicicação..: {str(traveler_list.placa).upper()}')
        print(f'   | {len(traveler_list.passageiros)} passageiro(s) encontrados.')
        print()
        if not data['error']:
            id = 1
            for traveler in traveler_list.passageiros:
                print(f' {id:3} {traveler.nome:40} {traveler.numero_doc:20} {traveler.orgao:10}')
                id += 1
        else:
            print(f'   * {data['error']}')
    else:
        print(f'   Ocorreu um erro ao abrir o arquivo "{join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME)}"')


def remove_list(placa: str, solicitacao: str):
    traveler_list = load_minimal_infor(placa.upper(), solicitacao)
    if traveler_list:
        print()
        print(f'   | Placa........: {str(traveler_list.placa).upper()}')
        print(f'   | Solicicação..: {traveler_list.num_solicitacao}')
        print(f'   | {len(traveler_list.passageiros)} passageiro(s) encontrados.')
        print()
        data = execute_remove(traveler_list)
        if not data['error']:
            print(f'   Passageiros excluidos com sucesso!')
    else:
        print(f'Ocorreu um erro ao abrir o arquivo "{join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME)}"')


def add_file(path: str):
    check_file = util.exist_file(path)
    if check_file['exist']:
        array_split_path = path.split('/')
        name_file = array_split_path[len(array_split_path) - 1]
        with open(join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR), encoding='utf-8') as my_json:
            json_data = json.load(my_json)
            path_workdir = json_data["workdir"]
            process_file({"name": name_file, "fullpath": path}, path_workdir)
    else:    
        print(check_file['message'])

def find_manifest(placa: str):
    traveler_list = load_minimal_infor(placa.upper(), "0000000000")
    if traveler_list:
        print()
        print(f'   | Placa...................: {str(traveler_list.placa).upper()}')
        data = execute_find_manifest(traveler_list)
        if not data['error']:
            print(f'   | Solicicações pendentes..: {data['manifests']}')
        print()
    else:
        print(f'Ocorreu um erro ao abrir o arquivo "{join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME)}"')
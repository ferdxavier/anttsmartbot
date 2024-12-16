import os, json, sys
from .spy import main_spy
from .features import describe_list, remove_list, add_file
from .tools.constants import ANTTSMARTBOT_CONFIGS_PATH, JSON_PAGES_MAP_FILE, \
                                JSON_AUTH_SITE_FILE_NAME, JSON_PATH_WORKDIR, \
                                DEFAULT_WORKDIR, DEFAULT_COMPANY, ID_PAGE

def init():
    if not os.path.exists(ANTTSMARTBOT_CONFIGS_PATH):
        os.mkdir(ANTTSMARTBOT_CONFIGS_PATH)
    if not os.path.exists(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME)):
        with open(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME) , "w") as file:
            json.dump(DEFAULT_COMPANY, file, indent=4)
    if not os.path.exists(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PAGES_MAP_FILE)):
        with open(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PAGES_MAP_FILE) , "w") as file:
            json.dump(ID_PAGE, file, indent=4)
    
    file_config_workdir = os.path.exists(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR))
    if not file_config_workdir:
        with open(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR) , "w") as file:
            json.dump(DEFAULT_WORKDIR, file, indent=4)
    
    with open(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR), encoding='utf-8') as my_json:
        json_data = json.load(my_json)
        path_workdir = json_data["workdir"]
        if not os.path.exists(path_workdir):
            os.mkdir(path_workdir)


    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++                      Seja bem vindo!!!                       ++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    init_process()

def init_remove_list():
    print("Remover a lista.")

def init_describe_list():
    print("Descrive os lista.")

def find_options(parametro):
    match parametro:
        case 'rm':
            return 'Comando inválido! Tente: "anttsmartbot rm [placa] [solicitação]"'
        case 'list':
            return 'Comando inválido! Tente: "anttsmartbot list [placa] [solicitação]"'
        case 'file':
            return 'Comando inválido! Tente: "anttsmartbot file [caminho do arquivo]"'
        case _:
            return 'Comando inválido! Tente: "anttsmartbot" ou "anttsmartbot [rm|list|file]"'


def init_process():
    if len(sys.argv) == 1:
        main_spy()
    else:
        if len(sys.argv) == 2:
            print(find_options(sys.argv[1]))
        if len(sys.argv) == 4:
            placa = sys.argv[2]
            solicitacao = sys.argv[3]
            if sys.argv[1] == 'list':
                describe_list(placa, solicitacao)
            elif sys.argv[1] == 'rm':    
                remove_list(placa, solicitacao)
        elif sys.argv[1] == 'file':
            add_file(sys.argv[2])
        else:
            print(f'Paramentos inválidos. Tente "anttsmartbot {sys.argv[1]} -help"')

if __name__ == "__main__":
    init()

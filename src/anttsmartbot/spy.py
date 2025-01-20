from time import sleep
from datetime import datetime
from .tools import util
from .processTravelerList import processList
from .tools.constants import ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR, JSON_AUTH_SITE_FILE_NAME
import json, os
from .bot import execute_add
from .tools.output import print_and_log

EXIT = False
TIME_SLEEP_DEFAULT = 2

def process_file(file, path_workdir):

    print("  ;-)")
    print_and_log(f'  | Arquivo......: {file["name"]}')
    data = processList(file["fullpath"])
    if not data["error"]:
        traveler_in_file = len(data["traveler_List"].passageiros)
        print_and_log(f'  | Placa........: {str(data["traveler_List"].placa).upper()}')
        print_and_log(f'  | Solicicacao..: {data["traveler_List"].num_solicitacao}')
        print_and_log(f'  | {traveler_in_file} passageiro(s) no registro.')
        print()
        
        salve_data = data['traveler_List']
        data = execute_add(data['traveler_List'])
        if not data['error']:
            traveler_solicitacao = data["summary"]["traveler_number_in_solicitacao"]
            traveler_lista = data["summary"]["traveler_number_in_list"]
            if traveler_in_file == traveler_lista:
                print_and_log(f'  * Arquivo processado com sucesso!')
                processed_files = []
                processed_files.append(file)
                util.move_processed_allowed_files(processed_files, path_workdir)
                print_and_log(f'  * Arquivo movido para "{path_workdir}/{util.DIR_NAME_SUCESS}"')
                with open( os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME), encoding='utf-8') as my_json:
                    json_data = json.load(my_json)
                
                    if not salve_data.placa in json_data["cars"]:
                        json_data["cars"].append(str(salve_data.placa).upper())
                        with open(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME) , "w") as my_json:
                            json.dump(json_data, my_json, indent=4)
            else:
                print_and_log(f'  * O número de passageiros digitados está diferente da lista. Verifique a lista "{file["fullpath"]}".')

            print_and_log(f'  * {traveler_lista} passageiro(s) digitalizado(s).')
            if traveler_lista != traveler_solicitacao:
                print_and_log(f'    * O número de passageiros no Manifesto é diferente da lista: {traveler_solicitacao} passageiro(s)')
        else:
            print(f'  * {data["error"]}')
        
    else:
        print("  # " +data["error"])

    sleep(0.5)

def main_process():
    try:
        with open(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR), encoding='utf-8') as my_json:
            json_data = json.load(my_json)
        path_workdir = json_data["workdir"]
        files =  util.list_files(path_workdir)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
        print("")
        print_and_log(f"  Pesquisa: {formatted_datetime}")
        if files:
            print_and_log(f'  {len(files)} arquivo(s) encontrado(s)!')
            file_denied_extensions = util.process_denied_extensions(files)
            if len(file_denied_extensions) > 0:
                print_and_log(f'  {len(file_denied_extensions)} arquivo(s) impróprio(s).')
                util.move_denied_extensions(file_denied_extensions, path_workdir)
                print_and_log(f'  * Arquivo(s) impróprio(s) movidos para "{path_workdir}/{util.DIR_NAME_DENIED}"')
            
            num_allow_files = len(files) - len(file_denied_extensions)
            print_and_log(f'  {num_allow_files} arquivo(s) aceito(s).')
            
            if num_allow_files > 0:
                print()
                print("  Processando as listas:")
                files =  util.list_files(path_workdir)
                
                for file in files:
                    process_file(file, path_workdir)

        else:
            print_and_log('  Nenhum arquivo encontrado!')
    except FileNotFoundError:
        print_and_log(f'  # Arquivo não encontrado: {os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR)}')
        
def main_spy():
    try:
        with open(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR), encoding='utf-8') as my_json:
            json_data = json.load(my_json)
        path_workdir = json_data["workdir"]
        print("")
        print_and_log(f'Lendo pasta de listas de passageiros "{path_workdir}".')
        print("")
        while not EXIT:  
            try:
                main_process()
                sleep(TIME_SLEEP_DEFAULT)
            except KeyboardInterrupt:
                break
        print("<<<<------------------------------------------------------------>>>>")
    except FileNotFoundError:
        print_and_log(f'  # Arquivo não encontrado: {os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR)}')
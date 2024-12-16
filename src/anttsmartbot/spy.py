from time import sleep
from datetime import datetime
from .tools import util
from .processTravelerList import processList
from .tools.constants import ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR
import json, os
from .bot import execute_add

EXIT = False
TIME_SLEEP_DEFAULT = 2

def process_file(file, path_workdir):

    print("  ;-)")
    print(f'      Processando o arquivo "{file["name"]}"')
    data = processList(file["fullpath"])
    if not data["error"]:
        traveler_in_file = len(data["traveler_List"].passageiros)
        print()
        print(f'        | Placa........: {data["traveler_List"].placa}')
        print(f'        | Solicicacao..: {data["traveler_List"].num_solicitacao}')
        print(f'        | {traveler_in_file} passageiro(s) no registro.')
        print()
        
        data = execute_add(data['traveler_List'])
        if not data['error']:
            traveler_solicitacao = data["summary"]["traveler_number_in_solicitacao"]
            traveler_lista = data["summary"]["traveler_number_in_list"]
            if traveler_in_file == traveler_lista:
                print(f'        * Arquivo processado com sucesso!')
            else:
                print(f'        * Passageiros digitados está diferente da lista. Verifique a lista "{file["fullpath"]}".')

            print(f'        * {traveler_lista} passageiro(s) digitalizado(s).')
            if traveler_lista != traveler_solicitacao:
                print(f'        * O número de passageiros no Manifesto é diferente da lista: {traveler_solicitacao} passageiro(s)')
        else:
            print(f'        * {data['error']:}')
            
        processed_files = []
        processed_files.append(file)
        util.move_processed_allowed_files(processed_files, path_workdir)
        print(f'        * Arquivo movido para "{path_workdir}/{util.DIR_NAME_SUCESS}"')
        print("")
        
    else:
        print("        # " +data["error"])
        if data["error"]:
            processed_files = []
            processed_files.append(file)
            util.move_processed_allowed_files(processed_files, path_workdir)
            print(f'        * Arquivo movido para "{path_workdir}/{util.DIR_NAME_SUCESS}"')

    sleep(1)

def main_process():
    with open(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR), encoding='utf-8') as my_json:
        json_data = json.load(my_json)
        path_workdir = json_data["workdir"]
        files =  util.list_files(path_workdir)
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
        print("")
        print(f"  Pesquisa: {formatted_datetime}")
        if files:
            print(f'  {len(files)} arquivo(s) encontrado(s)!')
            file_denied_extensions = util.process_denied_extensions(files)
            if len(file_denied_extensions) > 0:
                print(f'  {len(file_denied_extensions)} arquivo(s) impróprio(s).')
                util.move_denied_extensions(file_denied_extensions, path_workdir)
                print(f'      * Arquivo(s) impróprio(s) movidos para "{path_workdir}/{util.DIR_NAME_DENIED}"')
            
            num_allow_files = len(files) - len(file_denied_extensions)
            print(f'  {num_allow_files} arquivo(s) aceito(s).')
            
            if num_allow_files > 0:
                print()
                print("  Processando as listas:")
                files =  util.list_files(path_workdir)
                
                for file in files:
                    process_file(file, path_workdir)

        else:
            print('  Nenhum arquivo encontrado!')
        
def main_spy():
    with open(os.path.join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PATH_WORKDIR), encoding='utf-8') as my_json:
        json_data = json.load(my_json)
        path_workdir = json_data["workdir"]
        print("")
        print("<<<<------------------------------------------------------------>>>>")
        print("")
        print(f'  Lendo pasta de listas de passageiros "{path_workdir}".')
        print("")
        while not EXIT:  
            try:
                main_process()
                sleep(TIME_SLEEP_DEFAULT)
            except KeyboardInterrupt:
                break
        print("<<<<------------------------------------------------------------>>>>")
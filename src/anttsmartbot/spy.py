import time
from datetime import datetime
from .models import util
from .processTravelerList import processList

EXIT = False
PATH_LISTAS = '/home/fernando/listas'
TIME_SLEEP_DEFAULT = 2

def main_process():
    files =  util.list_files(PATH_LISTAS)
    print("")
    if files:
        print(f'  {len(files)} arquivo(s) encontrado(s)!')
        file_denied_extensions = util.process_denied_extensions(files)
        if len(file_denied_extensions) > 0:
            print(f'  {len(file_denied_extensions)} arquivo(s) impróprio(s).')
            util.move_denied_extensions(file_denied_extensions, PATH_LISTAS)
            print(f'      * Arquivo(s) impróprio(s) movidos para "{PATH_LISTAS}/{util.dir_name_denied}"')
        
        num_allow_files = len(files) - len(file_denied_extensions)
        print(f'  {num_allow_files} arquivo(s) aceito(s).')
        
        if num_allow_files > 0:
            print()
            print("  Processando as listas:")
            files =  util.list_files(PATH_LISTAS)
            for file in files:
                print("  ;-)")
                print(f'      Processando o arquivo "{file["name"]}"')
                data = processList(file["fullpath"])
                if not data["error"]:
                    traveler_solicitacao = data["summary"]["traveler_number_in_solicitacao"]
                    traveler_lista = data["summary"]["traveler_number_in_list"]
                    print()
                    print(f'        | Placa........: {data["traveler_List"].placa}')
                    print(f'        | Solicicacao..: {data["traveler_List"].num_solicitacao}')
                    print()
                    print(f'        * Arquivo processado com sucesso!')
                    print(f'        * {traveler_lista} passageiro(s) digitalizado(s).')
                    if traveler_lista != traveler_solicitacao:
                        print(f'        * O número de passageiros no Manifesto é diferente da lista: {traveler_solicitacao} passageiro(s)')
                    processed_files = []
                    processed_files.append(file)
                    util.move_processed_allowed_files(processed_files, PATH_LISTAS)
                    print(f'        * Arquivo movido para "{PATH_LISTAS}/{util.DIR_NAME_SUCESS}"')
                    print("")
                    
                else:
                    print("        # " +data["error"])
                    if data["error"]:
                        processed_files = []
                        processed_files.append(file)
                        util.move_processed_allowed_files(processed_files, PATH_LISTAS)
                        print(f'        * Arquivo movido para "{PATH_LISTAS}/{util.DIR_NAME_SUCESS}"')

                    
                time.sleep(1)
    else:
        print('  Nenhum arquivo encontrado!')
        
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%Y/%m/%d %H:%M:%S")
    print(f"   --> Pesquisa: {formatted_datetime}")
        
def main():
    print("")
    print("<<<<------------------------------------------------------------>>>>")
    print(f'  Lendo pasta de listas de passageiros "{PATH_LISTAS}".')
    print("")
    print(">")
    while not EXIT:  
        try:
            main_process()
            time.sleep(TIME_SLEEP_DEFAULT)
        except KeyboardInterrupt:
            break
    print("<<<<------------------------------------------------------------>>>>")

main()
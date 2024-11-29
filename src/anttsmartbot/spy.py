import time
from models import util
from processTravelerList import processList

exit = False
path_listas = '/home/fernando/listas'
time_sleep_default = 10

def main_process():
    print("<<<<---------------------------------->>>>")
    print(f'Lendo pasta de listas de passageiros "{path_listas}".')
    files =  util.list_files(path_listas)
    if files:
        print(f'{len(files)} arquivo(s) encontrado(s)!')
        
        file_denied_extensions = util.process_denied_extensions(files)
        print(f'{len(file_denied_extensions)} arquivo(s) impróprio(s).')
        util.move_denied_extensions(file_denied_extensions, path_listas)
        
        num_allow_files = len(files) - len(file_denied_extensions)
        print(f'{num_allow_files} arquivo(s) aceito(s).')
        
        if num_allow_files > 0:
            print()
            print("Processando as listas:")
            files =  util.list_files(path_listas)
            for file in files:
                print(f'    Processando o arquivo "{file["name"]}"')
                data = processList(file["fullpath"])
                if not data["error"]:
                    traveler_solicitacao = data["summary"]["traveler_number_in_solicitacao"]
                    traveler_lista = data["summary"]["traveler_number_in_list"]
                    print()
                    print(f'      | Placa........: {data["traveler_List"].placa}')
                    print(f'      | Solicicacao..: {data["traveler_List"].num_solicitacao}')
                    print()
                    print(f'      * Arquivo processado com sucesso!')
                    print(f'      * {traveler_lista} passageiro(s) digitalizado(s).')
                    if traveler_lista != traveler_solicitacao:
                        print(f'      * O número de passageiros no Manifesto é diferente da lista: {traveler_solicitacao} passageiro(s)')
                    processed_files = []
                    processed_files.append(file)
                    util.move_processed_allowed_files(processed_files, path_listas)
                    print(f'      * Arquivo movido para "{path_listas}/{util.dir_name_sucess}"')
                    
                    
                else:
                    print("      # " +data["error"])
                    
                time.sleep(1)
                print("")
    else:
        print('Nenhum arquivo encontrado!')

while not exit:  
    try:
        main_process()
        time.sleep(time_sleep_default)
    except KeyboardInterrupt:
        break
from models import util, model
from bot import execute
import json

def processList(path_traveler_list):
    check_file = util.exist_file(path_traveler_list)
    if check_file['exist']:
        data = model.load_traveler_List(path_traveler_list)
        if not data["error"]:
            with open("./anttsmartbot/json_auth_site.json", encoding='utf-8') as my_json:
                json_data = json.load(my_json)
                
            traveler_List = data["traveler_List"]
            traveler_List.cnpj = json_data["company"]
            traveler_List.senha = json_data["password"]
            traveler_List.site = json_data["site"]
            
            data = execute(traveler_List)
            
            data_ptl = data
            data_ptl["traveler_List"] = traveler_List
            
            return data_ptl
        else:
            return {"error": data["error"], "traveler_List": None}
            
    return {"error": check_file['message'], "traveler_List": None}

#print(processList('/home/fernando/afjldska.xlsx')["error"])
print(processList('/home/fernando/listas/TabelaDefaultListaPassageiro.xlsx')["error"])
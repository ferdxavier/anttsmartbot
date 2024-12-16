from .tools import util
from .models import model
import json
from os.path import join
from .tools.constants import ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME

def processList(path_traveler_list):
    check_file = util.exist_file(path_traveler_list)
    if check_file['exist']:
        data = model.load_traveler_List(path_traveler_list)
        if not data["error"]:
            with open( join(ANTTSMARTBOT_CONFIGS_PATH, JSON_AUTH_SITE_FILE_NAME), encoding='utf-8') as my_json:
                json_data = json.load(my_json)
                
                data["traveler_List"].cnpj = json_data["company"]
                data["traveler_List"].senha = json_data["password"]
                data["traveler_List"].site = json_data["site"]
                return data
        else:
            return {"error": data["error"], "traveler_List": None}
            
    return {"error": check_file['message'], "traveler_List": None}
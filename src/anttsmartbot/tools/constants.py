import os

ANTTSMARTBOT_CONFIGS_PATH = os.path.join(os.path.expanduser("~"), ".anttsmartbot")
JSON_AUTH_SITE_FILE_NAME = "json_auth_site.json"
JSON_PAGES_MAP_FILE = "json_pages_map.json"
JSON_PATH_WORKDIR = "json_path_workdir.json"

DEFAULT_COMPANY = {
    "company": "09511944000106", 
    "password": "420662",
    "site": "https://appweb1.antt.gov.br/autorizacaoDeViagem/AvPublico/Inicial.asp",
    "cars": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
}

ID_PAGE = {
    "home_page": "Sistema de Autorização de Viagem",
    "popup_page": "INFORMAÇÕES IMPORTANTES",
    "request_trip_page": "Sistema de Autorização de Viagem",
    "available_travel_options_page": "Opções Disponíveis",
    "request_list_page": "Listar Solicitação/Autorização de Viagem do Veículo",
    "manifest_page": "Consulta Solicitação de Viagem",
    "traveler_adder_page": "Para obter a Autorização de Viagem siga os passos abaixo", 
    "traveler_list_adder_page": "Relação de Passageiros da Solicitação de Viagem (Passo 2)"
}

DEFAULT_WORKDIR = {
    "workdir": os.path.join(os.path.expanduser("~"), "listas")
}

ALLOWS_COMMANDS = ["-rm", "", "", "", ""]
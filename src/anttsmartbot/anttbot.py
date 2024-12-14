import os, json
from .spy import main
from .processTravelerList import ANTTSMARTBOT_CONFIGS, JSON_AUTH_SITE_FILE_NAME

DEFAULT_COMPANY = {
    "company": "09511944000106", 
    "password": "420662",
    "site": "https://appweb1.antt.gov.br/autorizacaoDeViagem/AvPublico/Inicial.asp",
    "cars": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
}

def init():
    if not os.path.exists(ANTTSMARTBOT_CONFIGS):
        os.mkdir(ANTTSMARTBOT_CONFIGS)
    if not os.path.exists(os.path.join(ANTTSMARTBOT_CONFIGS, JSON_AUTH_SITE_FILE_NAME)):
        with open(os.path.join(ANTTSMARTBOT_CONFIGS, JSON_AUTH_SITE_FILE_NAME) , "w") as file:
            json.dump(DEFAULT_COMPANY, file, indent=4)

    print()
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("++++                      Seja bem vindo!!!                       ++++")
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    main()

if __name__ == '__main__':
    init()
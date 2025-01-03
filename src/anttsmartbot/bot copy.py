from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import Select
from .models import model
from .models.model import Passageiro
from .tools.constants import ANTTSMARTBOT_CONFIGS_PATH, JSON_PAGES_MAP_FILE, JSON_AUTH_SITE_FILE_NAME
import json, sys, time, os
from os.path import join
from selenium.webdriver.chrome.options import Options

# Configurações navegador headless
OPTIONS = Options()
OPTIONS.add_argument("--headless")
OPTIONS.add_argument("--disable-gpu")
OPTIONS.add_argument("--no-sandbox")

TIME_RECONNECT = 10
TIME_WAIT_SMALL = 0.017
NUM_ATTEMPTS_TO_ACESS_ELEMENT = 35
TRY_MANIFEST_PAGE = 7
TIME_TRY_MANIFEST_PAGE = 0.25
TIME_WAIT_ANOTHER_CLICK = 0.2
MANIFEST_PAGE = 'https://appweb1.antt.gov.br/autorizacaoDeViagem/AvPublico/solicitacao1.asp?cmdOpcao=Consultar&txtNumeroSolicitacao='
PATH_WEBDRIVER = "../../webdriver/chromedriver"
LOGIN_ERROR_MESSAGES = ["Informações incorretas. Por favor tente novamente.", "VEÍCULO NÃO HABILITADO.", "error '80020009'"]

def local_click(action):
    flag = True
    while flag:
        try:
            action.click()
            flag = False
        except NoSuchWindowException:
            time.sleep(TIME_WAIT_ANOTHER_CLICK)
        except NoSuchElementException:
            time.sleep(TIME_WAIT_ANOTHER_CLICK)

def set_passageiro(current_page, passageiro):
    time.sleep(0.05)
    current_page.find_element("xpath", '//*[@id="AutoNumber2"]/tbody/tr[4]/td[2]/input').send_keys(passageiro.nome)
    current_page.find_element("xpath", '//*[@id="telefone"]').send_keys(passageiro.telefone)
    combobox_select(current_page.find_element("xpath", '//*[@id="cmbMotivoViagem"]'), passageiro.situacao)
    if str(passageiro.crianca_colo).upper() == "SIM":
        current_page.find_element("xpath", '//*[@id="tdCriacaoColo"]/input').click()
    
    xpath_select_tipo_doc = None
    match str(passageiro.situacao).upper():
        case "BRASILEIRO CRIANÇA":
            xpath_select_tipo_doc = "2"
        case "ESTRANGEIRO":
            xpath_select_tipo_doc = "3"
        case "BRASILEIRO ADOLESCENTE":
            xpath_select_tipo_doc = "4"
        case _:
            xpath_select_tipo_doc = "1"

    combobox_select(current_page.find_element("xpath", f'//*[@id="cmbTipoDocumento{xpath_select_tipo_doc}"]'), passageiro.tipo_doc)
    current_page.find_element("xpath", '//*[@id="AutoNumber2"]/tbody/tr[9]/td[2]/input').send_keys(passageiro.numero_doc)
    current_page.find_element("xpath", '//*[@id="AutoNumber2"]/tbody/tr[10]/td[2]/input').send_keys(passageiro.orgao)
                 
def exist_traveler(current_page, passageiro):
    primary_key_down = str(str(passageiro.nome).strip() + str(passageiro.numero_doc).strip() + str(passageiro.orgao).strip()).upper()
    index = 2
    while True:
        try:
            nome = str(current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{index}]/td[2]').text).strip()
            numero_doc = str(current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{index}]/td[5]').text).strip()
            orgao = str(current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{index}]/td[6]').text).strip()
            primary_key_up = str(nome + numero_doc + orgao).upper()
            if primary_key_down == primary_key_up:
                return True 
            index = index + 1
        except NoSuchElementException:
            return False  

def find_travelers(current_page):
    index = 2
    passageiros = []
    while True:
        passageiro = Passageiro()
        try:
            nome = str(current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{index}]/td[2]').text).strip()
            numero_doc = str(current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{index}]/td[5]').text).strip()
            orgao = str(current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{index}]/td[6]').text).strip()

            passageiro.nome = nome
            passageiro.numero_doc = numero_doc
            passageiro.orgao = orgao

            passageiros.append(passageiro)
            index = index + 1
        except NoSuchElementException:
            return passageiros

def traveler_number_in_list_exec(current_page):
    index = 2
    while True:
        try:
            current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{index}]/td[2]')
            index = index + 1
        except NoSuchElementException:
            return index - 2
        
def combobox_select(element, value):
    if value and len(value) > 0 and value != 'nan':
        # Criar um objeto Select para interagir com o combobox
        select_object = Select(element)
        # Selecionar a opção pelo texto visível
        select_object.select_by_visible_text(value)

def exist_element(current_page, xpath):
    try:
        current_page.find_element("xpath", xpath)
        return True
    except NoSuchWindowException:
        return False
    except NoSuchElementException:
        return False

class NumberOffortExceeded(Exception):
    pass
class PageNotFoundExcept(Exception):
    pass

def find_element_by_xpath(current_page, xpath):
    attempt = 0
    while True:
        try:
            return current_page.find_element("xpath", xpath)
        except NoSuchElementException:
            if attempt == NUM_ATTEMPTS_TO_ACESS_ELEMENT:
                raise NumberOffortExceeded("Number of effort exceeded.")
        except NoSuchWindowException:
            if attempt == NUM_ATTEMPTS_TO_ACESS_ELEMENT:
                raise NumberOffortExceeded("Number of effort exceeded.")
        finally:
            time.sleep(TIME_WAIT_SMALL)
            attempt += 1
            
def is_page_valid_by_xpath(current_page, xpath, value):
    try:
        value_page = current_page.find_element("xpath", xpath).text
        if value_page == value:
            return True
        return True
    except NoSuchWindowException:
        return False
    except NoSuchElementException:
        return False
    
def get_current_page_url(current_page):
    return current_page.current_url

def exit_GUI():
    if 'DISPLAY' in os.environ:
        return True
    else:
        return False

def find_login_errors(current_page):
    xpath1 = "/html/body/p[1]/b"
    xpath2 = "/html/body/font"
    
    if exist_element(current_page,xpath1):
        if find_element_by_xpath(current_page,xpath1).text == LOGIN_ERROR_MESSAGES[0]:
            return "Verifique a senha."
        elif find_element_by_xpath(current_page,xpath1).text == LOGIN_ERROR_MESSAGES[1]:
            return "Veículo não habilitado."
    
    if exist_element(current_page,xpath2):
        if find_element_by_xpath(current_page,xpath2).text in LOGIN_ERROR_MESSAGES:
            return "CNPJ não habilitado"
    return None

def execute_login(traveler_List, json_data):
    # Carrega o webdriver ChromeDriver e abre a página
    # Navegador leadless
    current_page = webdriver.Chrome(OPTIONS)
    
    if exit_GUI():
        # Navegado comum com GUI (debug)
        current_page = webdriver.Chrome()
    
    current_page.get(traveler_List.site)
    #print(f'______________________home_page == {get_current_page_url(current_page)}')
    if not is_page_valid_by_xpath(current_page, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/i/b/font', json_data["home_page"]):
        return {"error": f'A página "{traveler_List.site}" não foi encontrada!', "current_page": None} 
    
    # Preenche o form para fazer o login e submet o formulário. E checa se a página aberta é válida e muda para ela
    find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[1]/td[3]/input').send_keys(traveler_List.cnpj)
    find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[2]/td[3]/input').send_keys(traveler_List.placa)
    find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[3]/td[3]/input').send_keys(traveler_List.senha)
    find_element_by_xpath(current_page, '//*[@id="btnEntrar"]').click()
    
    if not is_page_valid_by_xpath(current_page, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/i/b/font', json_data["request_trip_page"]):
        raise PageNotFoundExcept("Page not found: ")
    new_page = current_page.window_handles[len(current_page.window_handles) - 1]
    current_page.switch_to.window(new_page)

    error = find_login_errors(current_page)
    if error:
        return {"error": error, "current_page": None}
    return {"error": None, "current_page": current_page}

def go_traveler_list(traveler_List, json_data, current_page):
    # Redireciona para um tipo de viajem
    path_button_avancar = '//*[@id="AutoNumber2"]/tbody/tr[43]/td[2]/input[2]'
    if traveler_List.tipo_viagem == 'NORMAL':
        find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[8]/td[2]/a').click()
    else:
        find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[6]/td[2]/dd/a').click()
        #print(f'__available_travel_options_page == {get_current_page_url(current_page)}')
        if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/font/b', json_data["available_travel_options_page"]):
            return {"error": f'A página não foi encontrada! Local: available_travel_options_page', "summary": None} 
        find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[5]/td[4]/input').click()
        path_button_avancar = '//*[@id="AutoNumber2"]/tbody/tr[45]/td[2]/input[2]'
        
    #print(f'______________request_list_page == {get_current_page_url(current_page)}')
    if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["request_list_page"]):
        return {"error": f'A página não foi encontrada! Local: request_list_page', "summary": None} 
    
    # Procura pela solicitação desejada e a seleciona
    find_flag = False
    for x in range(2, 12):
        solicitacao = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[2]').text
        status = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[3]').text                                 
        if traveler_List.num_solicitacao == solicitacao:
            if str(status).upper() == "PENDENTE":
                find_element_by_xpath(current_page, f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[2]/a').click()
                find_flag = True
                break
            else:
                if str(status).upper() == "CANCELADA":
                    return {"error": f'A solicitação número {traveler_List.num_solicitacao} foi cancelada.', "summary": None}
                else:
                    return {"error": f'A solicitação número {traveler_List.num_solicitacao} já foi emitida.', "summary": None}
    if not find_flag:
        return {"error": f'A solicitação número {traveler_List.num_solicitacao} não foi encontrada.', "summary": None}
    
    try_manifest_page = 0
    #print(f'__________________manifest_page == {get_current_page_url(current_page)}')
    while not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["manifest_page"]):
        time.sleep(TIME_TRY_MANIFEST_PAGE)
        current_page.get(MANIFEST_PAGE +str(int(traveler_List.num_solicitacao)))
        if try_manifest_page > TRY_MANIFEST_PAGE:
            break
        try_manifest_page += 1
        
    #print(f'__________________manifest_page == {get_current_page_url(current_page)}')
    if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["manifest_page"]):
        return {"error": f'A página não foi encontrada! Local: manifest_page', "summary": None}
    
    # Pega o número de passageiros no manifesto e passa para a página a diante                                                                     
    traveler_number_in_solicitacao = int(str(find_element_by_xpath(current_page, '//*[@id="AutoNumber2"]/tbody/tr[36]/td[2]/input').get_attribute('value')))
    
    find_element_by_xpath(current_page, path_button_avancar).click()
    #print(f'____________traveler_adder_page == {get_current_page_url(current_page)}')
    if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["traveler_adder_page"]):
        return {"error": f'A página não foi encontrada! Local: traveler_adder_page', "summary": None} 
    
    find_element_by_xpath(current_page, '/html/body/p[6]/map/area[2]').click()

    #print(f'_______traveler_list_adder_page == {get_current_page_url(current_page)}')
    if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/font/b', json_data["traveler_list_adder_page"]):
        return {"error": f'A página não foi encontrada! Local: traveler_list_adder_page', "summary": None}
    
    return {"error": None, "current_page": current_page, "traveler_number_in_solicitacao": traveler_number_in_solicitacao} 

def execute_add(traveler_List: model.ListaViagem):
    with open(join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PAGES_MAP_FILE), encoding='utf-8') as my_json:
        json_data = json.load(my_json)
        while True:
            try:
                # Realiza o Login
                result_login = execute_login(traveler_List, json_data)
                if result_login['error']:
                    return {"error": result_login['error'], "summary": None}
                
                current_page = result_login["current_page"]

                # Vai até a lista de passageiros
                result_traveler_list = go_traveler_list(traveler_List, json_data, current_page)
                if result_traveler_list['error']:
                    return {"error": result_traveler_list['error'], "summary": None}
                
                current_page = result_traveler_list["current_page"]
                traveler_number_in_solicitacao = result_traveler_list["traveler_number_in_solicitacao"]
                
                existing_traveler = []
        
                for passageiro in traveler_List.passageiros:
                    if not exist_traveler(current_page, passageiro):
                        set_passageiro(current_page, passageiro)
                        find_element_by_xpath(current_page, '//*[@id="btnInc"]').click()

                        #print(f'_______traveler_list_adder_page == {get_current_page_url(current_page)}')
                        if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/font/b', json_data["traveler_list_adder_page"]):
                            return {"error": f'A página não foi encontrada! Local: traveler_list_adder_page', "summary": None}
                    else:
                        existing_traveler.append(passageiro)
                
                traveler_number_in_list = traveler_number_in_list_exec(current_page)
                current_page.close()
                return {"error": None, "summary": {"existing_traveler": existing_traveler, 
                                                "traveler_number_in_solicitacao": traveler_number_in_solicitacao, 
                                                "traveler_number_in_list": traveler_number_in_list}}
            except PageNotFoundExcept:
                time.sleep(TIME_RECONNECT)
            except NumberOffortExceeded:
                time.sleep(TIME_RECONNECT) 
            except WebDriverException:
                time.sleep(TIME_RECONNECT)
            except KeyboardInterrupt:
                break
    return {"error": f'Erro ao tentar abrir "{ open(join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PAGES_MAP_FILE)) }"', "summary": None}

def execute_list(traveler_List: model.ListaViagem):

    with open(join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PAGES_MAP_FILE), encoding='utf-8') as my_json:
        json_data = json.load(my_json)

    while True:
        try:
            # Carrega o webdriver ChromeDriver e abre a página
            # Navegador leadless
            current_page = webdriver.Chrome(OPTIONS)
            
            if exit_GUI():
                # Navegado comum com GUI (debug)
                current_page = webdriver.Chrome()
            
            current_page.get(traveler_List.site)
            #print(f'______________________home_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/i/b/font', json_data["home_page"]):
                return {"error": f'A página "{traveler_List.site}" não foi encontrada!', "summary": None} 
            
            # Preenche o form para fazer o login e submet o formulário. E checa se a página aberta é válida e muda para ela
            find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[1]/td[3]/input').send_keys(traveler_List.cnpj)
            find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[2]/td[3]/input').send_keys(traveler_List.placa)
            find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[3]/td[3]/input').send_keys(traveler_List.senha)
            find_element_by_xpath(current_page, '//*[@id="btnEntrar"]').click()
            
            if not is_page_valid_by_xpath(current_page, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/i/b/font', json_data["request_trip_page"]):
                raise PageNotFoundExcept("Page not found: ")
            new_page = current_page.window_handles[len(current_page.window_handles) - 1]
            current_page.switch_to.window(new_page)

            error = find_login_errors(current_page)
            print(error)
            if error:
                return {"error": error, "summary": None} 
            #print(f'______________request_trip_page == {get_current_page_url(current_page)}')
            
            # Redireciona para um tipo de viajem
            path_button_avancar = '//*[@id="AutoNumber2"]/tbody/tr[43]/td[2]/input[2]'
            find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[8]/td[2]/a').click()
            """
            if traveler_List.tipo_viagem == 'NORMAL':
                find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[8]/td[2]/a').click()
            else:
                find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[6]/td[2]/dd/a').click()
                #print(f'__available_travel_options_page == {get_current_page_url(current_page)}')
                if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/font/b', json_data["available_travel_options_page"]):
                    return {"error": f'A página não foi encontrada! Local: available_travel_options_page', "summary": None} 
                find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[5]/td[4]/input').click()
                path_button_avancar = '//*[@id="AutoNumber2"]/tbody/tr[45]/td[2]/input[2]'
                 
            #print(f'______________request_list_page == {get_current_page_url(current_page)}')
            """
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["request_list_page"]):
                return {"error": f'A página não foi encontrada! Local: request_list_page', "summary": None} 
               
            # Procura pela solicitação desejada e a seleciona
            find_flag = False
            for x in range(2, 12):
                solicitacao = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[2]').text
                status = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[3]').text                                 
                if traveler_List.num_solicitacao == solicitacao:
                    if str(status).upper() == "PENDENTE":
                        find_element_by_xpath(current_page, f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[2]/a').click()
                        find_flag = True
                        break
                    else:
                        if str(status).upper() == "CANCELADA":
                            return {"error": f'A solicitação número {traveler_List.num_solicitacao} foi cancelada.', "summary": None}
                        else:
                            return {"error": f'A solicitação número {traveler_List.num_solicitacao} já foi emitida.', "summary": None}
            if not find_flag:
                return {"error": f'A solicitação número {traveler_List.num_solicitacao} não foi encontrada.', "summary": None}
            
            try_manifest_page = 0
            #print(f'__________________manifest_page == {get_current_page_url(current_page)}')
            while not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["manifest_page"]):
                time.sleep(TIME_TRY_MANIFEST_PAGE)
                current_page.get(MANIFEST_PAGE +str(int(traveler_List.num_solicitacao)))
                try_manifest_page += 1
                if try_manifest_page < TRY_MANIFEST_PAGE:
                    break
                
            #print(f'__________________manifest_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["manifest_page"]):
                return {"error": f'A página não foi encontrada! Local: manifest_page', "summary": None}
            
            # Pega o número de passageiros no manifesto e passa para a página a diante                                                                     
            # traveler_number_in_solicitacao = int(str(find_element_by_xpath(current_page, '//*[@id="AutoNumber2"]/tbody/tr[36]/td[2]/input').get_attribute('value')))
            
            find_element_by_xpath(current_page, path_button_avancar).click()
            #print(f'____________traveler_adder_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["traveler_adder_page"]):
                return {"error": f'A página não foi encontrada! Local: traveler_adder_page', "summary": None} 
            
            find_element_by_xpath(current_page, '/html/body/p[6]/map/area[2]').click()

            #print(f'_______traveler_list_adder_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/font/b', json_data["traveler_list_adder_page"]):
                return {"error": f'A página não foi encontrada! Local: traveler_list_adder_page', "summary": None}
            
            traveler_List.passageiros = find_travelers(current_page)
            current_page.close()
            return {"error": None, "travelers":  traveler_List}
        
        except PageNotFoundExcept:
            time.sleep(TIME_RECONNECT)
        except NumberOffortExceeded:
            time.sleep(TIME_RECONNECT) 
        except WebDriverException:
            time.sleep(TIME_RECONNECT)
        except KeyboardInterrupt:
            break

def remove_travelers(current_page):
    attempt = 0
    while True:
        try:
            current_page.find_element("xpath", f'//*[@id="AutoNumber4"]/tbody/tr/td[1]/a/img').click()
            alert = current_page.switch_to.alert
            alert.accept()
        except NoSuchElementException:
            return True
        except NoSuchWindowException:
            if attempt == NUM_ATTEMPTS_TO_ACESS_ELEMENT:
                raise NumberOffortExceeded("Number of effort exceeded.")
        finally:
            time.sleep(TIME_WAIT_SMALL)
            attempt += 1
            


def execute_remove(traveler_List: model.ListaViagem):

    with open(join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PAGES_MAP_FILE), encoding='utf-8') as my_json:
        json_data = json.load(my_json)

    while True:
        try:
            # Carrega o webdriver ChromeDriver e abre a página
            # Navegador leadless
            current_page = webdriver.Chrome(OPTIONS)
            
            if exit_GUI():
                # Navegado comum com GUI (debug)
                current_page = webdriver.Chrome()
            
            current_page.get(traveler_List.site)
            #print(f'______________________home_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/i/b/font', json_data["home_page"]):
                return {"error": f'A página "{traveler_List.site}" não foi encontrada!', "summary": None} 
            
            # Preenche o form para fazer o login e submet o formulário. E checa se a página aberta é válida e muda para ela
            find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[1]/td[3]/input').send_keys(traveler_List.cnpj)
            find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[2]/td[3]/input').send_keys(traveler_List.placa)
            find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[3]/td[3]/input').send_keys(traveler_List.senha)
            find_element_by_xpath(current_page, '//*[@id="btnEntrar"]').click()
            
            if not is_page_valid_by_xpath(current_page, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/i/b/font', json_data["request_trip_page"]):
                raise PageNotFoundExcept("Page not found: ")
            new_page = current_page.window_handles[len(current_page.window_handles) - 1]
            current_page.switch_to.window(new_page)

            error = find_login_errors(current_page)
            print(error)
            if error:
                return {"error": error, "summary": None} 
            #print(f'______________request_trip_page == {get_current_page_url(current_page)}')
            
            # Redireciona para um tipo de viajem
            path_button_avancar = '//*[@id="AutoNumber2"]/tbody/tr[43]/td[2]/input[2]'
            find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[8]/td[2]/a').click()

            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["request_list_page"]):
                return {"error": f'A página não foi encontrada! Local: request_list_page', "summary": None} 
               
            # Procura pela solicitação desejada e a seleciona
            find_flag = False
            for x in range(2, 12):
                solicitacao = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[2]').text
                status = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[3]').text                                 
                if traveler_List.num_solicitacao == solicitacao:
                    if str(status).upper() == "PENDENTE":
                        find_element_by_xpath(current_page, f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[2]/a').click()
                        find_flag = True
                        break
                    else:
                        if str(status).upper() == "CANCELADA":
                            return {"error": f'A solicitação número {traveler_List.num_solicitacao} foi cancelada.', "summary": None}
                        else:
                            return {"error": f'A solicitação número {traveler_List.num_solicitacao} já foi emitida.', "summary": None}
            if not find_flag:
                return {"error": f'A solicitação número {traveler_List.num_solicitacao} não foi encontrada.', "summary": None}
            
            try_manifest_page = 0
            #print(f'__________________manifest_page == {get_current_page_url(current_page)}')
            while not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["manifest_page"]):
                time.sleep(TIME_TRY_MANIFEST_PAGE)
                current_page.get(MANIFEST_PAGE +str(int(traveler_List.num_solicitacao)))
                try_manifest_page += 1
                if try_manifest_page < TRY_MANIFEST_PAGE:
                    break
                
            #print(f'__________________manifest_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["manifest_page"]):
                return {"error": f'A página não foi encontrada! Local: manifest_page', "summary": None}
            
            # Pega o número de passageiros no manifesto e passa para a página a diante                                                                     
            # traveler_number_in_solicitacao = int(str(find_element_by_xpath(current_page, '//*[@id="AutoNumber2"]/tbody/tr[36]/td[2]/input').get_attribute('value')))
            
            find_element_by_xpath(current_page, path_button_avancar).click()
            #print(f'____________traveler_adder_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["traveler_adder_page"]):
                return {"error": f'A página não foi encontrada! Local: traveler_adder_page', "summary": None} 
            
            find_element_by_xpath(current_page, '/html/body/p[6]/map/area[2]').click()

            #print(f'_______traveler_list_adder_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/font/b', json_data["traveler_list_adder_page"]):
                return {"error": f'A página não foi encontrada! Local: traveler_list_adder_page', "summary": None}
            
            if remove_travelers(current_page):
                traveler_List.passageiros = []
            current_page.close()
            return {"error": None, "travelers":  traveler_List}
        
        except PageNotFoundExcept:
            time.sleep(TIME_RECONNECT)
        except NumberOffortExceeded:
            time.sleep(TIME_RECONNECT) 
        except WebDriverException:
            time.sleep(TIME_RECONNECT)
        except KeyboardInterrupt:
            break

def find_manifests(current_page, tipo_viagem):
 
    manifests = []
    for x in range(2, 12):
        solicitacao = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[2]').text
        status = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[3]').text                                 
        if str(status).upper() == "PENDENTE":
            manifests.append({"solicitacao": solicitacao, "tipo_viagem": tipo_viagem})

    return manifests

def execute_find_manifest(traveler_List):
    with open(join(ANTTSMARTBOT_CONFIGS_PATH, JSON_PAGES_MAP_FILE), encoding='utf-8') as my_json:
        json_data = json.load(my_json)
    while True:
        try:
            # Carrega o webdriver ChromeDriver e abre a página
            # Navegador leadless
            current_page = webdriver.Chrome(OPTIONS)
            
            if exit_GUI():
                # Navegado comum com GUI (debug)
                current_page = webdriver.Chrome()
            
            current_page.get(traveler_List.site)
            #print(f'______________________home_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/i/b/font', json_data["home_page"]):
                return {"error": f'A página "{traveler_List.site}" não foi encontrada!', "summary": None} 
            
            # Preenche o form para fazer o login e submet o formulário. E checa se a página aberta é válida e muda para ela
            find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[1]/td[3]/input').send_keys(traveler_List.cnpj)
            find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[2]/td[3]/input').send_keys(traveler_List.placa)
            find_element_by_xpath(current_page, '/html/body/div[2]/form/table[1]/tbody/tr[3]/td[3]/input').send_keys(traveler_List.senha)
            find_element_by_xpath(current_page, '//*[@id="btnEntrar"]').click()
            
            if not is_page_valid_by_xpath(current_page, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/i/b/font', json_data["request_trip_page"]):
                raise PageNotFoundExcept("Page not found: ")
            new_page = current_page.window_handles[len(current_page.window_handles) - 1]
            current_page.switch_to.window(new_page)

            error = find_login_errors(current_page)
            if error:
                return {"error": error, "summary": None} 
            
            #print(f'______________request_trip_page == {get_current_page_url(current_page)}')
            
            # Redireciona para um tipo de viajem
            find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[8]/td[2]/a').click()
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["request_list_page"]):
                return {"error": f'A página não foi encontrada! Local: request_list_page', "summary": None}
            manifests = find_manifests(current_page, "NORMAL")
            
            find_element_by_xpath(current_page, '//*[@id="AutoNumber2"]/tbody/tr/td[1]/input').click()
            if not is_page_valid_by_xpath(current_page, '/html/body/table[2]/tbody/tr[2]/td[2]/table/tbody/tr[1]/td/i/b/font', json_data["request_trip_page"]):
                raise PageNotFoundExcept("Page not found: ")
            
            find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[6]/td[2]/dd/a').click()
            #print(f'__available_travel_options_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/font/b', json_data["available_travel_options_page"]):
                return {"error": f'A página não foi encontrada! Local: available_travel_options_page', "summary": None} 
            find_element_by_xpath(current_page, '//*[@id="AutoNumber1"]/tbody/tr[5]/td[4]/input').click()

            manifests += find_manifests(current_page, "ATIPICA")
            current_page.close()
            return {"error": None, "manifests": manifests}
        
        except PageNotFoundExcept:
            print("Erro 1")
            time.sleep(TIME_RECONNECT)
        except NumberOffortExceeded:
            print("Erro 2")
            time.sleep(TIME_RECONNECT) 
        except WebDriverException:
            print("Erro 3")
            time.sleep(TIME_RECONNECT)
        except KeyboardInterrupt:
            break

# 629
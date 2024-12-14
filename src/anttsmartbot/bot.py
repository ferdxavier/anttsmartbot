from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException, NoSuchElementException, WebDriverException
from selenium.webdriver.support.ui import Select
from .models import model
import time
import json
from selenium.webdriver.chrome.options import Options

# Configurações navegado leadless
OPTIONS = Options()
OPTIONS.add_argument("--headless")
OPTIONS.add_argument("--disable-gpu")
OPTIONS.add_argument("--no-sandbox")

def local_click(action):
    flag = True
    while flag:
        try:
            action.click()
            time.sleep(0.15)
            flag = False
        except NoSuchWindowException:
            time.sleep(0.5)
        except NoSuchElementException:
            time.sleep(0.5)

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
            
                
def exit_traveler(current_page, passageiro):
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

    
    
TIME_RECONNECT = 10
TIME_WAIT_SMALL = 0.02
NUM_ATTEMPTS_TO_ACESS_ELEMENT = 30
TRY_MANIFEST_PAGE = 5
TIME_TRY_MANIFEST_PAGE = 0.4
MANIFEST_PAGE = 'https://appweb1.antt.gov.br/autorizacaoDeViagem/AvPublico/solicitacao1.asp?cmdOpcao=Consultar&txtNumeroSolicitacao='
PATH_WEBDRIVER = "../../webdriver/chromedriver"

def execute(traveler_List: model.ListaViagem):
    with open("json_pages_map.json", encoding='utf-8') as my_json:
        json_data = json.load(my_json)
    while True:
        try:
            # Carrega o webdriver ChromeDriver e abre a página
            # Navegador leadless
            #current_page = webdriver.Chrome(OPTIONS)
            
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
            #print(f'______________request_trip_page == {get_current_page_url(current_page)}')
            
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
                solicitacao = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[2]/a').text
                status = current_page.find_element("xpath", f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[3]').text                                             
                if traveler_List.num_solicitacao == solicitacao:
                    if str(status).upper() == "PENDENTE":
                        find_element_by_xpath(current_page, f'//*[@id="AutoNumber3"]/tbody/tr[{x}]/td[2]/a').click()
                        find_flag = True
                        break
                    else:
                        if status == "Cancelada":
                            return {"error": f'A solicitação número {traveler_List.num_solicitacao} foi cancelada.', "summary": None}
                        else:
                            return {"error": f'A solicitação número {traveler_List.num_solicitacao} já foi emitida.', "summary": None, "emitida": True}
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
            traveler_number_in_solicitacao = int(str(find_element_by_xpath(current_page, '//*[@id="AutoNumber2"]/tbody/tr[36]/td[2]/input').get_attribute('value')))
            
            find_element_by_xpath(current_page, path_button_avancar).click()
            #print(f'____________traveler_adder_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/h4', json_data["traveler_adder_page"]):
                return {"error": f'A página não foi encontrada! Local: traveler_adder_page', "summary": None} 
            
            find_element_by_xpath(current_page, '/html/body/p[6]/map/area[2]').click()

            #print(f'_______traveler_list_adder_page == {get_current_page_url(current_page)}')
            if not is_page_valid_by_xpath(current_page, '/html/body/table[3]/tbody/tr/td/font/b', json_data["traveler_list_adder_page"]):
                return {"error": f'A página não foi encontrada! Local: traveler_list_adder_page', "summary": None}
            
            existing_traveler = []
    
            for passageiro in traveler_List.passageiros:
                if not exit_traveler(current_page, passageiro):
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
    
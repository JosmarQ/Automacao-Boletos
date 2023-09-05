from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pandas as pd
import time

def Open_Browser():
    global driver
    service = Service(executable_path='./chromedriver.exe')
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com")

def Load_Excel(path):
    global df
    df = pd.read_excel(path)

def Loop():
    for index, row in df.iterrows():
        nome_contato = row['Nome']
        numero_contato = row['Número']
        numero_pagina = row['Número da Página']
        with open('mensagem.txt', encoding='utf8') as msg:
            mensagem = msg.read()
            mensagem = mensagem.format(nome=nome_contato, pagina=numero_pagina)
        # Abrir a conversa com o contato
        driver.get(f"https://web.whatsapp.com/send?phone={numero_contato}")
        time.sleep(5)  # Aguarde para garantir que a página esteja totalmente carregada

        # Inserir a mensagem e enviar
        input_box = driver.find_element("xpath",'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
        input_box.send_keys(mensagem)
        input_box.send_keys(Keys.ENTER)
        time.sleep(2)

        # Clicar na opção de anexo
        attachment_box = driver.find_element("xpath",'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div/span')
        attachment_box.click()
        time.sleep(2)

        # Pegar o caminho do PDF correspondente
        nome_do_mes = datetime.now().strftime('%B')
        filepath = f'C:\\Users\mathe\OneDrive\Área de Trabalho\AutomacaoBoletosCondominio\\boletos\{nome_do_mes}\page_{numero_pagina}.pdf'

        # Selecionar o PDF
        image_box = driver.find_element("xpath",'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[1]/li/div/input')
        image_box.send_keys(filepath)
        time.sleep(2)

        # Enviar o PDF
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(('xpath','//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')))
        send_button = driver.find_element('xpath','//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')
        send_button.click()
        time.sleep(2)
    driver.quit()
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from separar import separar_pdf


separar_pdf()

# Inicialize o navegador
service = Service(executable_path='./chromedriver.exe')
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://web.whatsapp.com")

# Aguarde até que o usuário faça o login no WhatsApp Web manualmente
input("Faça o login no WhatsApp Web e pressione Enter para continuar...")

# Carregue os dados do Excel
import pandas as pd
df = pd.read_excel('PlanilhaCondominos.xlsx')

# Loop através dos contatos e envie as mensagens
for index, row in df.iterrows():
    nome_contato = row['Nome']
    numero_contato = row['Número']
    numero_pagina = row['Número da Página']
    mensagem = f"Olá {nome_contato}, testando."

    # Abra a conversa com o contato
    driver.get(f"https://web.whatsapp.com/send?phone={numero_contato}")
    time.sleep(5)  # Aguarde para garantir que a página esteja totalmente carregada

    # Insira a mensagem e envie
    input_box = driver.find_element("xpath",'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
    input_box.send_keys(mensagem)
    input_box.send_keys(Keys.ENTER)
    time.sleep(1)

    nome_do_mes = datetime.now().strftime('%B')
    filepath = f'C:\\Users\mathe\OneDrive\Área de Trabalho\AutomacaoBoletosCondominio\\boletos\{nome_do_mes}\page_{numero_pagina}.pdf'
    attachment_box = driver.find_element("xpath",'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div/span')
    attachment_box.click()
    time.sleep(1)

    image_box = driver.find_element("xpath",'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/ul/div/div[1]/li/div/input')
    image_box.send_keys(filepath)
    time.sleep(1)

    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(('xpath','//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')))
    send_button = driver.find_element('xpath','//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')
    send_button.click()
    time.sleep(1)

# Feche o navegador
input("Finalizado. Pressione Enter para fechar.")
driver.quit()
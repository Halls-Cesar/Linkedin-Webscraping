from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import csv
import pandas as pd
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
from datetime import datetime

chrome_options = Options()
#chrome_options.add_argument("--headless") # Executa em background, sem abrir a janela do Chrome

# Define o caminho do driver do Chrome e inicializa o navegador
url = "https://www.linkedin.com/jobs/search?keywords=Marketing%20E%20Publicidade&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'"
#url_de_testes = 'https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&position=4&pageNum=0&currentJobId=3543396686'
caminho = r'C:\Users\raulc\OneDrive\Área de Trabalho\projeto\desafio\chromedriver.exe'
#caminho = r'K:\ProjetosPython\Projetos\Desafio\Raul Cesar Marques de Farias\chromedriver.exe'	#caminho solicitado
driver = webdriver.Chrome(options=chrome_options, executable_path=caminho)
driver.get(url)
time.sleep(3)
driver.maximize_window()    #maximiza a tela para melhor execucao do codigo

# Espera ate algo aparecer na tela, como o botão de aceitar cookies. Se a tela carregar e não aparecer retorna uma mensagem de que não apareceu.
try:
    cookie_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.artdeco-button--primary[data-tracking-control-name="accept_all"]')))
    cookie_button.click()
except:
    print("O botão de aceitar os cookies não apareceu")

# define os filtros das vagas
tipo_de_vaga = driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[4]/div/div/button')
tipo_de_vaga.click()
time.sleep(2)
tmp_integral = driver.find_element(By.ID, 'f_JT-0')
tmp_integral.click()
time.sleep(2)
button1 = driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form/ul/li[4]/div/div/div/button')
button1.click()
time.sleep(5)
exp = driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form[1]/ul/li[5]/div/div/button')
exp.click()
estagio = driver.find_element(By.ID, 'f_E-0')
time.sleep(2)
estagio.click()
time.sleep(2)
button2 = driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form[1]/ul/li[5]/div/div/div/button')
button2.click()
time.sleep(5)
tipo_de_vaga1 = driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form[1]/ul/li[2]/div/div/button')
tipo_de_vaga1.click()
time.sleep(2)
estagio1 = driver.find_element(By.XPATH, '//*[@id="f_JT-3"]')
estagio1.click()
time.sleep(2)
button1 = driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form[1]/ul/li[2]/div/div/div/button')
button1.click()
time.sleep(2)
exp1 = driver.find_element(By.XPATH,'/html/body/div[1]/section/div/div/div/form[1]/ul/li[3]/div/div/button')
exp1.click()
time.sleep(2)
estagio2 = driver.find_element(By.XPATH, '//*[@id="f_E-0"]')
estagio2.click()
time.sleep(2)
button3 = driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form[1]/ul/li[3]/div/div/div/button')
button3.click()
time.sleep(10)


#scroll da pagina ate o final e clica no botao 'ver mais vagas'
i = 1
while i <= 20:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    i=i+1
    time.sleep(3)
    try:
        x = driver.find_element(By.XPATH, "//button[@aria-label='Ver mais vagas']")
        x.click()
        time.sleep(3)
    except:
        pass
        time.sleep(4)

soup = BeautifulSoup(driver.page_source, "html.parser")
time.sleep(3)

#encontra todas as vagas e cria um arquivo para alocar os dados
jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
with open('Scraping-Raul Cesar Marques de Farias.csv', 'w', encoding='utf8', newline='') as f:

    writer = csv.writer(f)
    header = ['URL da Vaga', 'Nome da Vaga', 'Nome da Empresa', 'URL da Empresa', 'Tipo de Contratacao', 'Nivel de Experiencia', 'Numero de Candidaturas', 'Data da Postagem da Vaga', 'Horario da Realizacao do Scraping']
    writer.writerow(header)
    #encontra todos as vagas da pagina
    for job in jobs:

        url_vagas = job.find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]').get("href")

        if url_vagas != None:

            url_empresa = job.find('a', class_='hidden-nested-link').get("href")
            nome_empresa = job.find('h4', class_='base-search-card__subtitle').get_text().strip()
            nome_vaga = job.find('h3', class_='base-search-card__title').get_text().strip()
            
        
            driver.get(url_vagas)
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            ul = soup.find('ul', class_='description__job-criteria-list')
            spans = ul.find_all('span', class_='description__job-criteria-text description__job-criteria-text--criteria')   
            nivel_experiencia = ""
            tipo_emprego = ""

            for span in spans:
                h3 = span.find_previous('h3', class_='description__job-criteria-subheader')
                if h3.text.strip() == "Nível de experiência":
                    nivel_experiencia = span.text.strip()
                    if nivel_experiencia == "Assistente":
                        nivel_experiencia = "Estagio"
                elif h3.text.strip() == "Tipo de emprego":
                    tipo_emprego = span.text.strip()

            sections = soup.find_all('div', class_='topcard__flavor-row')
            for section in sections:
    
                content = section.find_next('span', class_='posted-time-ago__text topcard__flavor--metadata')
                if content != None:
                    data_postagem = content.get_text().strip()
                else:
                    data_postagem = 'Data nao encontrada'
                
                        
            divs = soup.find_all('div', class_='face-pile flex see-who-was-hired')
            for div in divs:
                prev1 = div.find_previous('figcaption')
                prev2 = div.find_previous('span')

                candidaturas = ''

                if prev1 != None:
                    candidaturas = prev1.get_text().strip()
                elif prev2 != None:
                    candidaturas = prev2.get_text().strip()

            driver.back()
        else:
            pass

        #data da realizacao do scraping
        d = datetime.now()
        data_scraping = d.strftime('%d/%m/%Y %H:%M')

        lista = ([url_vagas, nome_vaga, nome_empresa, url_empresa, tipo_emprego , nivel_experiencia, candidaturas, data_postagem, data_scraping])
        writer.writerow(lista)
        time.sleep(5)
        

driver.close()
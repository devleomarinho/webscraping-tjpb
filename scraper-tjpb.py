from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://www.tjpb.jus.br/comarcas/lista")

comarcas_info = {}

WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'link-modal-comarca')))
comarcas = driver.find_elements(By.CLASS_NAME, 'link-modal-comarca')

for comarca in comarcas:
    municipio = comarca.text.strip()
    if municipio:
        print(f"Buscando informações para {municipio}...")
    else:
        print("Nome da cidade vazio")
        continue

    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(comarca)).click()
        time.sleep(5)

        jurisdicoes = {}

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'content'))
        )

        table_rows = driver.find_elements(By.XPATH, '//table[@class="table table-condensed"]/tbody/tr')
        for row in table_rows:
            unidade = row.find_element(By.XPATH, './td[1]').text.strip()
            juiz = row.find_element(By.XPATH, './td[2]').text.strip()
            jurisdicoes[unidade] = juiz

        comarcas_info[municipio] = {'jurisdicoes': jurisdicoes}

    except Exception as e:
        print(f"Erro ao buscar as informações para {municipio}: {e}")

    finally:

        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'close'))
        )
        close_button.click()
        time.sleep(2)

driver.quit()

dados = []
for municipio, info in comarcas_info.items():
    for unidade, juiz in info['jurisdicoes'].items():
        dados.append({'Municipio': municipio, 'Unidade': unidade, 'Juiz': juiz})

df = pd.DataFrame(dados)

df.to_csv('comarcas_info.csv', index=False)
df.to_json('comarcas_info.json', orient='split', indent=4, index=False, force_ascii=False)

print("Dados salvos em 'comarcas_info.csv'")

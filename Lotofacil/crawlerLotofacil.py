from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import numpy as np

database = pd.DataFrame(columns=['Concurso', 'Numeros', 'Ganhadores'])
concurso = 2109

driver = webdriver.Chrome('LOTOFÁCIL/chromedriver')
driver.get('http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil')

for i in range(concurso):
    time.sleep(4.5)
    numeros = driver.find_elements_by_class_name("ng-binding.dezena.ng-scope")
    #numeros[2].text
    resultado = []
    for indice in range(len(numeros)):
        resultado.append(int(numeros[indice].text))
        
    ganhadores = driver.find_elements_by_class_name("description.ng-binding.ng-scope")
    wins = ganhadores[0].text
    winst = wins.split("\n")
    winst = winst[1][0:2]
    print(concurso, winst)
    if winst == 'Nã':
        wins = 0
    else:
        wins = int(winst)
    
    database = database.append({'Concurso': concurso,  'Numeros': resultado,
                                'Ganhadores': wins}, ignore_index = True)
    concurso -=1    
    
    buscaConcurso = driver.find_element_by_id("buscaConcurso")
    buscaConcurso.clear() #limpa o input da busca do concurso
    buscaConcurso.send_keys(concurso)
    buscaConcurso.send_keys(Keys.RETURN)
    
driver.close()
    
database.to_csv('lotofacil_all.csv', index=False)

    




    ''' ------------ AREA DE TESTE -------------'''
   
driver = webdriver.Chrome('LOTOFÁCIL/chromedriver')
driver.get('http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil')

ganhadores = driver.find_elements_by_class_name("description.ng-binding.ng-scope")
wins = ganhadores[0].text
winst = wins.split("\n")
winst = winst[1][0:2]

driver.close()


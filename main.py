import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import os



def parse(site):
    result_list = {'author': [], 'title': []}
    s = Service('webdr/chromedriver.exe')
    driver = webdriver.Chrome(service=s)
    
    driver.get(site)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(20)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    
    authors = driver.find_elements(By.CLASS_NAME, 'art__author')
    titles = driver.find_elements(By.CLASS_NAME, 'art__name')


    for author, title in zip(authors, titles):
        if len(author.text) > 0:
            result_list['author'].append(author.text)
            newtitle = ''
            for letter in title.text:
                if letter != '\n':
                    newtitle += letter
            result_list['title'].append(newtitle)

    driver.close()

    if not os.path.exists('results'):
        os.mkdir('results')
    unix = str(time.strftime('%d-%m-%Y'))
    folder = f'results/{unix}'
    if not os.path.exists(folder):
        os.mkdir(folder)

    file_name = f'{folder}/litres.csv'

    df = pd.DataFrame(data=result_list)
    df.to_csv(file_name, mode='a', encoding='cp1251')


site = 'https://www.litres.ru/novie/elektronnie-knigi/?lang=52'

if __name__ == '__main__':
    parse(site)



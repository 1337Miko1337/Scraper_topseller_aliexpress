from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
driver = webdriver.Chrome()
driver.get('https://www.ukr.net/')
elems = driver.find_elements(By.CLASS_NAME, 'feed__section')
print('elems: ',elems)
headers_news = []
name_news = []
flag = False
for el in elems:
    elem = el.find_element(By.TAG_NAME, 'a').text
    headers_news.append(elem)
    if flag:
        elem = el.find_elements(By.CLASS_NAME, 'feed__item--title')
        name_news.append(elem)
    elif not flag:
        elem = el.find_elements(By.TAG_NAME, 'li')
        name_news.append(elem)
        flag = True
print('head: ', headers_news)
for i in range(len(headers_news)-1):
    print(headers_news[i])
    for j in name_news[i]:
        print(j.text)
    print('\n')

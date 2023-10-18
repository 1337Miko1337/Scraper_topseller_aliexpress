from selenium import webdriver
from bs4 import BeautifulSoup
import re
import pymysql

# scrape information
driver = webdriver.Chrome()
driver.get('https://rozetka.com.ua/notebooks/c80004/') # link to site
soup = BeautifulSoup(driver.page_source, 'html.parser')
names = soup.find_all(class_='goods-tile__heading ng-star-inserted')
prices = soup.find_all(class_='goods-tile__price--old price--gray ng-star-inserted')
currency = soup.find_all('span', class_='currency')
connection = pymysql.connect(host='127.0.0.1', password='admin', user='root', port=3306, database='notebooks',
                             cursorclass=pymysql.cursors.DictCursor) # connect to MySQL database, my database placed in localhost
cursor = connection.cursor()
min_len = min(len(names), len(prices))
# info processing
for i in range(min_len):
    print('names: ', names)
    name = names[i]['title']
    name = name.replace('"', '')
    link = names[i]['href']
    print('link: ', link)
    driver.get('' + link + 'characteristics/')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # to scrape characteristic of product we get link to page of product and redirect to characteristics
    description_label = soup.find_all(attrs={'class': 'characteristics-full__label'})
    desc_value = soup.find_all(class_='characteristics-full__value')
    str_tmp = ''
    for j in range(len(description_label)):
        tmp = desc_value[j].find(class_='characteristics-full__sub-list').find(class_='ng-star-inserted').find(
            class_='ng-star-inserted')
        str_tmp += description_label[j].get_text() + ' : ' + tmp.get_text() + ' '
        str_tmp = str_tmp.replace('"', '')
    tmp_price = re.findall(r'(\d+).(\d\d+)', prices[i].get_text())
    price = tmp_price[0][0] + tmp_price[0][1] + currency[i].get_text()
    insert_query = '"' + name + '","' + price + '","' + str_tmp[:] + '"'
    insert_query = 'insert into notebook VALUES(null,' + insert_query + ')'
    cursor.execute(insert_query)
    connection.commit()

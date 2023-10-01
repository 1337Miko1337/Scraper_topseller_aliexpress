from selenium import webdriver
from bs4 import BeautifulSoup
import csv
from time import sleep


driver = webdriver.Chrome()
driver.get("https://campaign.aliexpress.com/wow/gcp-plus/ae/tupr?_immersiveMode=true&wx_navbar_hidden=true&wx_navbar_transparent=true&ignoreNavigationBar=true&wx_statusbar_hidden=true&wh_weex=true&wh_pid=300000444/nWKxQjK5Sx&spm=a2g0o.tm1000001522.6946203670.title&aecmd=true")
sleep(3)
soup = BeautifulSoup(driver.page_source, 'html.parser')
names = soup.find_all('span', class_='rax-text-v2 prodTitle rax-text-v2--overflow-hidden rax-text-v2--singleline')
prices = soup.find_all('span', class_="rax-text-v2 rax-text-v2--overflow-hidden rax-text-v2--singleline")
fields = ['Name', 'Price']
file = open('base.csv', 'a', newline='')
writer = csv.DictWriter(file, fields)
for i in range(len(names)):
    while '%' in prices[i].get_text():
        prices.pop(i)
    scraped_info = {'Name': names[i].get_text(), 'Price': prices[i].get_text()}
    writer.writerow(scraped_info)
file.close()

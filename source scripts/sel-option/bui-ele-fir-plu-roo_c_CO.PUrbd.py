#****************
# Web Data Scrape
# http://www.prbd.com/searches/consearch.php
# Stewart Spencer
#****************

import csv, re, requests, time, string, codecs
from bs4 import BeautifulSoup
from glob import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from time import sleep

f = codecs.open('bui-ele-fir-plu-roo_c_CO.PUrbd_%s_000.csv' %(time.strftime('%Y%m%d')),'w','UTF-8')

headers = ["number_type","company_flag","licensee_type_cd","entity_name", "examinee", "address1", "city", "state", "zip", "phone", "insurance_expiration", "work_comp_expiration", "expiration_date"]
f.write("\"" + "\",\"".join(headers) + "\"\n")

#path_to_chromedriver = '/Users/Anthony/Documents/drivers/chromedriver'
browser = webdriver.Chrome(glob('C:\\Users\\*\\Downloads\\chromedriver.exe'))
url = 'http://www.prbd.com/searches/consearch.php'

for i in range(0,46):
    print i
    browser.get(url)

    element1 = browser.find_elements_by_tag_name('option')
    element2 = browser.find_element_by_xpath('/html/body/div[1]/form[2]/table[2]/tbody/tr/td/input')
    licensee_type = element1[i].text

    element1[i].click()
    element2.click()

    soup = BeautifulSoup(browser.page_source)
    
    info = []
    start = False
    for tr in soup.find_all('tr'):
        info.append("")
        info.append('1')
        info.append(licensee_type)
        
        for td in tr.find_all('td'):
            info.append(td.text)
        if info[3] == "Name":
            start = True
        if (start == True and info[3] != "Name"):
            f.write("\"" + "\",\"".join(info) + "\"\n")
            print("\"" + "\",\"".join(info) + "\"\n")
        info = []
    print i
browser.close()
f.close()

#**********************************
# Web Scrape
# https://ilesonline.idfpr.illinois.gov/Lookup/LicenseLookup.aspx
#
# Stewart Spencer
# 10/06/1014
#**********************************

import csv, re, requests, time, string, codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from time import sleep

stamp = time.strftime("%Y%m%d")

name = 'gen_c_ILfpr_' + stamp + '_000.csv'

f = codecs.open(name, 'w', 'UTF-8')

headers = ["entity_name", "address", "DBA", "license_number", "licensee_type_cd", "status", "first_issue_date", "Effective Date", "expiration_date","number_type","company_flag"]
f.write("\"" + "\"|\"".join(headers) + "\"\n") 



browser = webdriver.PhantomJS()

url = 'https://ilesonline.idfpr.illinois.gov/Lookup/LicenseLookup.aspx'

time.sleep(1)

cds = ['104000000']

cdstop = ['104016900']

i = 0
k = 0

info = []
bool1 = True

for j in range(0, len(cds)):
    while bool1 == True:
        browser.get(url)
        
        element1 = browser.find_element_by_xpath('//*[@id="MainContentPlaceHolder_ucLicenseLookup_ctl01_tbCredentialNumber_Credential"]')
        element2 = browser.find_element_by_xpath('//*[@id="btnLookup"]')

        element1.clear()
        key = int(cds[j])+k
        element1.send_keys(str(key).zfill(9))
        element2.click()

        time.sleep(2)
        element3 = browser.find_elements_by_tag_name('a')
        if len(element3) > 11:
            element3[5].click()
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source)        

            for tr in soup.find_all('tr'):
                for td in tr.find_all('td'):
                    if(i == 1 or i == 3):
                        info.append(td.text)
                i = i+1
                
            if(len(info) > 1):
                info.append('License Number')
                info.append('1')
                print("\"" + "\"|\"".join(info) + "\"\n")
                f.write("\"" + "\"|\"".join(info) + "\"\n")
            info = []                
        
        i = 0
        k = k + 1
        if int(key) == int(cdstop[j]):
            bool1 = False
    bool1 = True
    k = 0
f.close()
browser.close





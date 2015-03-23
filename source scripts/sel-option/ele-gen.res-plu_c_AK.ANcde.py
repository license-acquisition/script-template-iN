#**********************************************************************************
# Web Scrape 
# http://bsd.muni.org/contractorlicensing/#Search
#
# Stewart Spencer
# 10/03/2014
#**********************************************************************************


import csv, re, requests, time, string, codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from glob import glob
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from time import sleep

def checker(info, item, j):
    while j < len(item):
        if info[0] == item[j]:
            return False
        j = j+1
    return True
stamp = time.strftime("%Y%m%d")
f = codecs.open('ele-gen.res-plu_c_AK.ANcde_' + stamp + '_000.csv', 'w', 'UTF-8')

headers = ["number_type","company_flag","entity_name","phone", "license_number","licensee_type_cd","expiration_date","license2","license_type_2","expiration_date2","license3","license_type3","expiration_date3","license4","license_type4","expiration_date4"]
f.write("|".join(headers) + "\n")

browser = webdriver.Chrome()
#browser = webdriver.PhantomJS()
url = 'http://bsd.muni.org/contractorlicensing/#Search'

for k in range(1): #originally 1->87
    browser.get(url)
    #element1 = browser.find_elements_by_tag_name('option')
    element2 = browser.find_element_by_xpath('//*[@id="btnSearch"]')
    #element1[k].click()
    element2.click()

    soup = BeautifulSoup(browser.page_source)
    table = soup.find_all('table')

    info = []
    info2 = []
    info3 = []
    item = []
    i = 0
    j = 0
    test = True
    #print len(table[10].find_all('tr'))
    if len(table) > 10:
        for tr in table[10].find_all('tr'):
            string = ""
            for td in tr.find_all('td'):
                info.append(td.text)
            test = checker(info, item, j)
            if test == True:
                while i < len(info) :
                    if (i+1)%3 == 0:
                        item.append(info[i])
                    i = i+1
            if(test == True and len(info) > 2):
                info.pop(1)
                info2 = re.split('[(]',info[0])
                if len(info2) == 1:
                    info2.append('')
                if len(info2) > 2:
                    for l in range(0,len(info2)-1):
                        string = string + info2[l]
                    last = info2[len(info2)-1]
                    info2 = []
                    info2.append(string)
                    info2.append(last)
                    info2[1] = '(' + info2[1]
                info.pop(0)
                info3 = []
                info3.append('License Number')
                info3.append('1')
                info3 = info3 + info2 + info
                f.write("|".join(info3) + "\n")
                #print("\"" + "\",\"".join(info3) + "\"\n")
                #print('***********')
                #print 'got it'
            test = True
            info = []
            info2 = []
            info3 = []
            i = 0
            j = 0
    print 'done'

browser.close()
f.write('Done \n')
f.close()
browser.quit()

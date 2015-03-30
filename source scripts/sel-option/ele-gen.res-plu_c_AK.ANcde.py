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
from script_template import create_file, logger

def checker(info, item, j):
    while j < len(item):
        if info[0] == item[j]:
            return False
        j = j+1
    return True

f = create_file('ele-gen.res-plu_c_AK.ANcde', 'w', ['102', '6', '12', '33', '21', '32', '13', '27', '22', '14', '28', '23', '15', '29', '24', '16'])
l = logger('ele-gen.res-plu_c_AK.ANcde')
driver = webdriver.PhantomJS()

def main():
    url = 'http://bsd.muni.org/contractorlicensing/#Search'
    for k in range(1): #originally 1->87
        driver.get(url)
        #element1 = driver.find_elements_by_tag_name('option')
        element2 = driver.find_element_by_xpath('//*[@id="btnSearch"]')
        #element1[k].click()
        element2.click()

        soup = BeautifulSoup(driver.page_source)
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
                    l.info(info3)

                test = True
                info = []
                info2 = []
                info3 = []
                i = 0
                j = 0
        l.info('done')


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
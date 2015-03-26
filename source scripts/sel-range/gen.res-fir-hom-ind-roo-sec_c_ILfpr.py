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
from script_template import create_file, logger

f = create_file('gen.res-fir-hom-ind-roo-sec_c_ILfpr', 'w', ['12', '0', '10', '21', '32', '37', '19', 'Effective Date', '13', '102', '6'])
l = logger('gen.res-fir-hom-ind-roo-sec_c_ILfpr')
driver = webdriver.PhantomJS()

def main():
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
            driver.get(url)
            
            element1 = driver.find_element_by_xpath('//*[@id="MainContentPlaceHolder_ucLicenseLookup_ctl01_tbCredentialNumber_Credential"]')
            element2 = driver.find_element_by_xpath('//*[@id="btnLookup"]')

            element1.clear()
            key = int(cds[j])+k
            element1.send_keys(str(key).zfill(9))
            element2.click()

            time.sleep(2)
            element3 = driver.find_elements_by_tag_name('a')
            if len(element3) > 11:
                element3[5].click()
                time.sleep(1)
                soup = BeautifulSoup(driver.page_source)        

                for tr in soup.find_all('tr'):
                    for td in tr.find_all('td'):
                        if(i == 1 or i == 3):
                            info.append(td.text)
                    i = i+1
                    
                if(len(info) > 1):
                    info.append('License Number')
                    info.append('1')
                    l.info(info)
                    f.write("\"" + "\"|\"".join(info) + "\"\n")
                info = []                
            
            i = 0
            k = k + 1
            if int(key) == int(cdstop[j]):
                bool1 = False
        bool1 = True
        k = 0

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
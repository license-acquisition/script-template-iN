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
from script_template import create_file, logger

f = create_file('bui-ele-fir-plu-roo_c_CO.PUrbd', 'w', ['102', '6', '32', '12', 'examinee', '0', '4', '36', '44', '33', '73', '85', '13'])
l = logger('bui-ele-fir-plu-roo_c_CO.PUrbd')
driver = webdriver.PhantomJS()

def main():
    url = 'http://www.prbd.com/searches/consearch.php'
    for i in range(0,46):
        l.debug(i)
        driver.get(url)

        element1 = driver.find_elements_by_tag_name('option')
        element2 = driver.find_element_by_xpath('/html/body/div[1]/form[2]/table[2]/tbody/tr/td/input')
        licensee_type = element1[i].text

        element1[i].click()
        element2.click()

        soup = BeautifulSoup(driver.page_source)
        
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
                f.write("|".join(info) + "\n")
                l.info(infO)
            info = []
        l.info(i)


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
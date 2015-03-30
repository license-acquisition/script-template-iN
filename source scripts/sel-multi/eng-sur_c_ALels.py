#*************************
# Web Scrape
# http://bels.alabama.gov/ComResults.aspx
# Stewart Spencer
# 10/15/2014
#*************************



import csv, re, requests, time, string, codecs
from bs4 import BeautifulSoup
from glob import glob
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from time import sleep
from script_template import create_file, logger

f = create_file('eng-sur_c_ALels', 'w', ['12', '21', '0', '4', '36', '44', '32', '37', '62', '19', '20', '13', '102', '6'])
l = logger('eng-sur_c_ALels')
driver = webdriver.PhantomJS()

def main():
    url = 'http://bels.alabama.gov/comSearch.aspx'
    driver.get(url)
    driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_Submit"]').click()
    k = 2
    first = True
    while True:
        try:
            soup = BeautifulSoup(driver.page_source)
            table = soup.find_all('table')
            info = []
            lst = []
            lst = re.split('\n',table[0].text)
            j = 0
            for i in range(0, len(lst)):
                if lst[i][0:1]!='1' and lst[i][0:1]!= '.' and lst[i][0:5] != 'Click' and len(lst[i])>2:
                    j = j + 1
                    line = re.split(':', lst[i])
                    if len(line) > 2:
                        for l in range(2, len(line)):
                            line[1] = line[1] + line[l]
                    if len(line) > 1 and j!=3:
                        info.append(line[1])
                    if len(line) == 1 and j!=3:
                        info.append(line[0])
                    
                    if j == 3:
                        nline = re.split('[,]',line[1])
                        address = nline[0]
                        city = nline[1]
                        state_zip = re.sub(' ','',nline[2])
                        state = state_zip[0:2]
                        zip_ = state_zip[2:]
                        info.append(address)
                        info.append(city)
                        info.append(state)
                        info.append(zip_)
                        
                    if j % 9 == 0:
                        j = 0
                        info.append('License Number')
                        info.append('1')
                        f.write("\"" + "\",\"".join(info) + "\"\n")
                        l.info(info)
                        info = []
            next_ = '//*[@id="ContentPlaceHolder1_GridView1"]/tbody/tr[1]/td/table/tbody/tr/td['+str(k)+']/a'
            k += 1
            if k == 12 and first == True:
                k = 3
                first = False
            if k == 13 and first == False:
                k = 3
            time.sleep(1)
            driver.find_element_by_xpath(next_).click()
            l.debug(k)
        except Exception as e:
            l.error(str(e))
            break

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
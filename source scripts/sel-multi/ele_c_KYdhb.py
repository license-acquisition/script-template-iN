import sys, requests, time, re, csv, codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.ui as UI
count = 1

start=time.time()

f=codecs.open('ele_c_KYdhb_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')

f.write('|'.join(["license_number", "entity_name", "expiration_date", "licensee_type_cd", "status", "city", "county","state", "company_flag"]) +'\n')
browser = webdriver.Chrome() 
browser.implicitly_wait(1)
browser.get('http://dhbc.ky.gov/bce/ei/el/Pages/default.aspx')
browser.get('https://ky.joportal.com/License/Search')
Select(browser.find_element_by_id("Division")).select_by_visible_text("Electrical Licensing")
#changetohvachere
browser.implicitly_wait(1)
browser.find_element_by_xpath("//button[@type='button']").click()
browser.implicitly_wait(1)
browser.find_element_by_css_selector("#ui-multiselect-LicenseType-option-0").click()
browser.implicitly_wait(1)
browser.find_element_by_id("btnSubmit").click()
time.sleep(3)
#browser.find_element_by_css_selector("input.ui-pg-input").clear()
#browser.find_element_by_css_selector("input.ui-pg-input").send_keys("1092").send_keys("Keys.ENTER")
keys = browser.find_element_by_xpath("//*[@id='licenseSearchGridPagingBar_center']/table/tbody/tr/td[8]/select")
keys.send_keys('50' + 'Keys.RETURN') #grab 50 results per page
#elem = browser.find_element_by_css_selector("input.ui-pg-input")
#elem.clear
#elem.send_keys('1092' + 'Keys.RETURN')
time.sleep(1)
#browser.send_keys("Keys.ENTER")
#browser.find_element_by_css_selector("span.ui-icon.ui-icon-seek-next").send_keys("Keys.ENTER")
while count < 7:
        print ' - - - - - - %s of 400 - - - - - - ' %count
        time.sleep(5)
        #browser.wait_element_to_be_present
        c = browser.page_source
        soup = BeautifulSoup(c)
        matt = soup.findAll("tbody")[3]
        trs = soup.findAll("tbody")[3]
        for tr in trs:
                info = []
                tds = tr.findAll("td")
                try:
                        info.append(tds[2].text) # licnum
                        info.append(tds[3].text) # name
                        info.append(tds[4].text) # expdate
                        info.append(tds[5].text) # typecd
                        info.append(tds[6].text) # status
                        info.append(tds[7].text) # city
                        for td in tds[8].text.split(','):
                                info.append(td.strip()) # county and state
                        info.append('1') # company flag
                        print info
                        f.write('|'.join(info) + '\n')
                except:
                        continue
        time.sleep(5)
        browser.find_element_by_css_selector("span.ui-icon.ui-icon-seek-next").click()
        time.sleep(5)
        count += 1
        
browser.close()
f.close()

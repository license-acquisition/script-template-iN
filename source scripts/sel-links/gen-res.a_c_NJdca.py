from bs4 import BeautifulSoup
import urllib
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
import codecs
from datetime import date
year = date.today().year
month = date.today().month
day = date.today().day

page = 1
count = 1
f= codecs.open('gen-res.a_c_NJdca_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')

headers = ["entity_name", "city", "state", "licensee_type_cd", "license_number", "status", "cause", "first_issue_date", "expiration_date", "company_flag", "number_type", "city_flag", "county_flag"]
f.write("\"" + "\",\"".join(headers) + "\"\n")


g=open('UrlListNJ-locksmith_c.csv', 'w')
link_list = []
driver = webdriver.PhantomJS()
driver.get("https://newjersey.mylicense.com/verification/Search.aspx?facility=Y")
#Select(driver.find_element_by_id("t_web_lookup__license_type_name")).select_by_visible_text("Locksmith Business")
driver.find_element_by_css_selector("option[value=\"Locksmith Business\"]").click()
#wait for element to appear
time.sleep(1)
driver.find_element_by_id("sch_button").click()


while page < 10000:
    print (page)
    soup = BeautifulSoup(driver.page_source)
    links = soup.findAll("a")
    for link in links:
        if "Details" in link['href']:
            link_list.append(link['href'])
            g.write(str(link) + ' ' + '\n')



    
    fail = 0
    while fail < 4:
        
        try:
                if page == 40:
                        driver.find_element_by_xpath("//*[@id='datagrid_results']/tbody/tr[42]/td/a[40]").click()
                        time.sleep(2)
                        page = page + 1
                        fail = 5
                       
                        
                else:
                    if page % 40 != 0:
                        page = page + 1
                        driver.find_element_by_link_text(str(page)).click()
                        time.sleep(1)
                        fail = 5
                        
                                            
                                            
                    else:
                        driver.find_element_by_xpath("//*[@id='datagrid_results']/tbody/tr[42]/td/a[41]").click()
                        page = page + 1
                        fail = 5
                        
                                            
        except:
            fail = fail + 1
            time.sleep(1)
            if fail == 4:                    
                print ('script failed on' + str(page))
                page = page + 100000
            else:
                print ('failing')
g.close()
for x in link_list:
        count = count + 1
        try:
            url = 'https://newjersey.mylicense.com/verification/' + x
            driver.get(url)
            soup = BeautifulSoup(driver.page_source)
            
            name = str(soup.find(id="full_name"))
            start = name.find('>') + 1
            end = name[3:].find('<') + 3
            name = name[start:end]
            name = re.sub(',','',name)
            print (name)


            city = str(soup.findAll(id="addr_city"))
            start = city.find('>') + 1
            end = city[3:].find('<') + 3
            city = city[start:end]

            state = str(soup.findAll(id="addr_state"))
            start = state.find('>') + 1
            end = state[3:].find('<') + 3
            state = state[start:end]

            license_type = str(soup.findAll(id="license_type"))
            start = license_type.find('>') + 1
            end = license_type[3:].find('<') + 3
            license_type = license_type[start:end]

            license_no = str(soup.findAll(id="license_no"))
            start = license_no.find('>') + 1
            end = license_no[3:].find('<') + 3
            license_no = license_no[start:end]
                    
            status = str(soup.findAll(id="sec_lic_status"))
            start = status.find('>') + 1
            end = status[3:].find('<') + 3
            status = status[start:end]

            cause = str(soup.findAll(id="changeReason"))
            start = cause.find('>') + 1
            end = cause[3:].find('<') + 3
            cause = cause[start:end]

            issue = str(soup.findAll(id="issue"))
            start = issue.find('>') + 1
            end = issue[3:].find('<') + 3
            issue = issue[start:end]

            exp = str(soup.findAll(id="expiration_date"))
            start = exp.find('>') + 1
            end = exp[3:].find('<') + 3
            exp = exp[start:end]

            company_flag = "1"
            number_type = "License Number"



            #data = (name + ',', city + ',', state + ',', license_type + ',', license_no + ',', status + ',', cause + ',', issue + ',', exp + ',', url + '\n')
            info = [name, city, state, license_type, license_no, status, cause, issue, exp, company_flag, number_type]
            if count % 4 == 0:
                print ('good one!')
            else:
                if count % 3 == 0:
                    print ('It worked!!')
                else:
                    print ('BOO YAA')
            
            f.write("\"" + "\",\"".join(info) + "\"\n")

            info = []
        except:
            print ('Por Que!?!?!')


f.close()
driver.close()
driver.quit()
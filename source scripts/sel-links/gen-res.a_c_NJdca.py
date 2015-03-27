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
from script_template import create_file, logger

f = create_file('gen-res.a_c_NJdca', 'w', ['12', '4', '36', '32', '21', '37', 'cause', '19', '13', '6', '102', '5', '9'])
l = logger('gen-res.a_c_NJdca')
g = codecs.open('gen-res.a_c_NJdca_links.csv', 'w', 'utf-8')
driver = webdriver.PhantomJS()

def main():
    page = 1
    count = 1
    driver.get("https://newjersey.mylicense.com/verification/Search.aspx?facility=Y")
    driver.find_element_by_css_selector("option[value=\"Locksmith Business\"]").click()
    time.sleep(1) #wait for element to appear
    driver.find_element_by_id("sch_button").click()

    while page < 10000:
        print (page)
        soup = BeautifulSoup(driver.page_source)
        links = soup.findAll("a")
        for link in links:
            if "Details" in link['href']:
                l.info(link['href'])
                g.write(str(link['href']) + '\n')

        fail = 0
        while fail < 4:       
            try:
                    if page == 40:
                            driver.find_element_by_xpath("//*[@id='datagrid_results']/tbody/tr[42]/td/a[40]").click()
                            time.sleep(2)
                            page += 1
                            fail = 5                      
                            
                    else:
                        if page % 40 != 0:
                            page += 1
                            driver.find_element_by_link_text(str(page)).click()
                            time.sleep(1)
                            fail = 5                                          
                                                
                        else:
                            driver.find_element_by_xpath("//*[@id='datagrid_results']/tbody/tr[42]/td/a[41]").click()
                            page += 1
                            fail = 5
                                                                       
            except:
                fail = fail + 1
                time.sleep(1)
                if fail == 4:                    
                    l.error('script failed on' + str(page))
                    page = page + 100000
                else:
                    l.error('failing')
    g.close()

    for x in open('gen-res.a_c_NJdca_links.csv', 'r'):
            count = count + 1
            try:
                url = 'https://newjersey.mylicense.com/verification/' + x
                soup = BeautifulSoup(requests.get(url).content)
                
                info = []
                info.append(soup.find_all('span', {'id': 'full_name'})[0].text.strip())
                info.append(soup.find_all('span', {'id': 'addr_city'})[0].text.strip())
                info.append(soup.find_all('span', {'id': 'addr_state'})[0].text.strip())
                info.append(soup.find_all('span', {'id': 'license_type'})[0].text.strip())
                info.append(soup.find_all('span', {'id': 'license_no'})[0].text.strip())
                info.append(soup.find_all('span', {'id': 'sec_lic_status'})[0].text.strip())
                info.append(soup.find_all('span', {'id': 'changeReason'})[0].text.strip())
                info.append(soup.find_all('span', {'id': 'issue'})[0].text.strip())
                info.append(soup.find_all('span', {'id': 'expiration_date'})[0].text.strip())
                info.append("1")
                info.append('License Number')
                
                if count % 4 == 0:
                    l.info('good one!')
                else:
                    if count % 3 == 0:
                        l.info('It worked!!')
                    else:
                        l.info('BOO YAA')
                        
                f.write("|".join(info) + "\n")

                info = []
            except Exception as e:
                l.error(str(e))


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
# **********************
# Web Scrape of NJ Architect Companies
# Site: https://newjersey.mylicense.com/verification/Search.aspx?facility=Y

# Modified for recurrence by Anthony Nault
# 9/3/2014
# **********************

##STeven Y
##New Jersery, State Level.  Architects.  Companies.
##NJ has a terrible website and its portal takes forever.  THis script will be a pain in the ass.
##Its a pretty easy script though, all things considered.  I each entry has a unique url, however, they are random.  THis method will get them all
##I go through page by page and collect all of the urls (this part will take hours)
##then I simply go to each link.
##I collected all the links first and then went to the page rather than going to the url as i got the links.
##I did this because the page navigation is soooooo slow, but the page by page navigation is pretty fast
##If it crashes while I'm getting the links, i can restart it much faster.

from bs4 import BeautifulSoup
import urllib
import requests
import codecs
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re
from script_template import create_file, logger

f = create_file('arc_c_NJdca', 'w', ['12', '4', '36', '32', '21', '37', 'cause', '19', '13', '6', '102', '5', '9'])
l = logger('arc_c_NJdca')
g = codecs.open('arc_c_NJdca_links.csv', 'w', 'utf-8')
driver = webdriver.PhantomJS()

def main():
    page = 1
    count = 1

    # Gather link URLs. This takes a long time. Then use the URLs get data!
    driver.get("https://newjersey.mylicense.com/verification/Search.aspx?facility=Y")
    Select(driver.find_element_by_id("t_web_lookup__profession_name")).select_by_visible_text("Architecture")
    driver.find_element_by_css_selector("option[value=\"Architecture\"]").click()
    driver.find_element_by_id("sch_button").click()
    while page < 10000:
        l.debug(page)
        soup = BeautifulSoup(driver.page_source)
        links = soup.findAll("a")
        for link in links:
            if "Details" in link['href']:
                #link_list.append(link['href'])
                g.write(str(link) + '\n')

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
                fail += 1
                time.sleep(1)
                if fail == 4:                    
                    l.error('script failed on' + str(page))
                    page += 100000
                else:
                    l.debug('failing')
    g.close()

    # We have a file full of links. Now lets PARSE!
    for x in open('arc_c_NJdca_links', 'r'):
            count += 1
            try:
                url = 'https://newjersey.mylicense.com/verification/' + x
                soup = BeautifulSoup(requests.get(url).content)
                
                info = []
                info.append(soup.find_all('span', {'id': 'full_name'})[0].text)
                info.append(soup.find_all('span', {'id': 'addr_city'})[0].text)
                info.append(soup.find_all('span', {'id': 'addr_state'})[0].text)
                info.append(soup.find_all('span', {'id': 'license_type'})[0].text)
                info.append(soup.find_all('span', {'id': 'license_no'})[0].text)
                info.append(soup.find_all('span', {'id': 'sec_lic_status'})[0].text)
                info.append(soup.find_all('span', {'id': 'changeReason'})[0].text)
                info.append(soup.find_all('span', {'id': 'issue'})[0].text)
                info.append(soup.find_all('span', {'id': 'expiration_date'})[0].text)
                info.append("1")
                info.append('License Number')

                if count % 4 == 0:
                    l.info('good one!')
                else:
                    if count % 3 == 0:
                        l.info('It worked!!')
                    else:
                        l.info('BOO YAA')
                
                f.write("\"" + "\",\"".join(info) + "\"\n")
                l.info(info)
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
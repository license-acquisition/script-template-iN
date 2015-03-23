# -*- coding: cp1252 -*-

import requests, re, time, codecs, sys
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits
import time
start=time.time()
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open('eng-sur_c_LApel_20150305_000.csv', 'a', 'utf-8')
f.write("entity_name,license_number,status,first_issue_date,expiration_date,supervisor,supervisee,address1,state,zip,company_flag\n")

driver =webdriver.Chrome()
driver.get("https://renewals.lapels.com/Lookup/LicenseLookup.aspx")

optionList = [2,8]
dataOption = [0,2,3,4,5,6,7]


for number in optionList:
    page = 166
    fail = 0
    driver.find_elements_by_tag_name("option")[number].click()
    driver.find_element_by_id("btnLookup").click()
    time.sleep(3)
    if number == 2:
        page = 166
        driver.find_element_by_partial_link_text("...").click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text("...")[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text("...")[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text("...")[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_elements_by_partial_link_text('...')[1].click()
        time.sleep(3)
        driver.find_element_by_link_text('166').click()
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source)

    while fail<1:
        try:
            links = driver.find_elements_by_tag_name('a')

            for i in range (15,40): #range of relevant links for each page
                try:
                    info = []
                    if page == 33:  #freaky test for third line of data on page 33. avoid data using this condition.
                        if i == 17:
                            page += 1
                            continue
                    if page > 10:
                        links[i+1].click() # i + 1 because starting from page 11 onwards we have an extra ("...") partial links.
                    else:
                        links[i].click()
                    time.sleep(1)
                    soup = BeautifulSoup(driver.page_source)
                    content = soup.find("div", id="ctl00_OutsidePlaceHolder_ucLicenseDetailPopup_UpdatePanel1")      

                    for i in dataOption:
                        info.append(content.findAll('td')[i].text.replace(u'\xa0',u''))
                    
                    info[4] = (re.sub(u"Â",u'',re.sub('\xa0','',(info[4]))))
                    info[5] = (re.sub(u"Â",u'',re.sub('\xa0','',(info[5]))))
                    info[6] = (re.sub(u"Â",u'',re.sub('\xa0','',(info[6]))))
                    info.append("1")
                    info[7] = content.findAll('td')[1]
                    info[7] = re.sub("<br/>",' ',str(info[7]))
                    info[7] = (re.sub("<td>",'',re.sub('</td>','',(info[7]))))
                    info[7] = "\",\"".join(info[7].rsplit(" ", 1))
                    info[7] = "\",\"".join(info[7].rsplit(", ", 1))

                    info.append("1")
                    print ("\"" + "\",\"".join(info) + "\"\n")
                    f.write("\"" + "\",\"".join(info) + "\"\n")
                    time.sleep(3)
                    driver.find_element_by_id("ctl00_OutsidePlaceHolder_ucLicenseDetailPopup_linkToCloseLicDet").click()
                except Exception, e:
                    print str(e)
                
                    if "can\'t decode byte 0xc3" in str(e):
                        time.sleep(3)
                        driver.find_element_by_id("ctl00_OutsidePlaceHolder_ucLicenseDetailPopup_linkToCloseLicDet").click()
                        pass
                    
            
            page = page + 1

            time.sleep(1)
           
            if page == 11:
                time.sleep(1)
                driver.find_element_by_partial_link_text("...").click()
                time.sleep(1)
            elif page % 10 == 1:
                time.sleep(1)
                driver.find_elements_by_partial_link_text("...")[1].click()
                time.sleep(1)
            else:
                time.sleep(1)
                driver.find_element_by_link_text(str(page)).click()
                time.sleep(1)       
            print page

        except Exception,e:
            print str(e)
            fail = fail + 1


f.close()

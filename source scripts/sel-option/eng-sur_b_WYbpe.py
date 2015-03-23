import sys, requests, codecs, time, re, csv, string
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits
start=time.time()
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open('eng-sur_b_WYbpe_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')
headers=["last",]
f.write("name,number_type|company_name|Contact|Business|Business2|address1|address2|city|state|zip|Foreign|license_number|Branch|licensee_type_cd|Corp|expiration_date|first_issue_date|status|company_flag\n")

#driver = webdriver.Chrome()
driver = webdriver.PhantomJS()

#soup = BeautifulSoup(driSelever.page_source)

#again=soup.find("option")

driver.get("http://engineersroster.wyo.gov/rosterSearch.aspx")

for k in range(1,6):
    driver.find_elements_by_tag_name("option")[k].click()
    #driver.find_element_by_css_selector("#cboType").click()
    #driver.find_element_by_css_selector("#cboType > option:nth-child(%d)"%k).click()
    driver.find_element_by_css_selector("#submit").click()

    soup = BeautifulSoup(driver.page_source)

    table1 = soup.find('table', id='gvResults')

    tri = table1.find_all('tr')


    
    tr = soup.findAll("tr",{"style":"color:#333333;background-color:#F7F6F3;","style":"color:#284775;background-color:White;"})
    tl = soup.findAll("tr",{"style":"color:#284775;background-color:White;"})
    for ok in tr:
        info = []
        first = ok.findAll('td')[0].text
        last = ok.findAll('td')[1].text
        fullname = first + " " + last
        info.append("".join(i for i in fullname if ord(i)<128))
        info.append("registration number")
       
            

        for td in ok.findAll('td')[2:]:
            info.append("".join(i for i in td.text if ord(i)<128))
        

        if len(info[2])>1:
            info.append("1")

        else:
            info.append("")

            

        f.write("|".join(info) + "\n")
				
        print "\"" + "\",\"".join(info) + "\"\n"

        info=[]
    for ok in tl:
        info = []
        first = ok.findAll('td')[0].text
        last = ok.findAll('td')[1].text
        fullname = first + " " + last
        info.append("".join(i for i in fullname if ord(i)<128))
        info.append("registration number")
        

        for td in ok.findAll('td')[2:]:
            info.append("".join(i for i in td.text if ord(i)<128))
            

        if len(info[2])>1:
            info.append("1")

        else:
            info.append("")

            

        f.write("|".join(info) + "\n")
				
        print "\"" + "\",\"".join(info) + "\"\n"

        info=[]
f.close()
driver.close()
driver.quit()

'''info.append("1")
                    info.append("license number")
                    info.append("1")
'''

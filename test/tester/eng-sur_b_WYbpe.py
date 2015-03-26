import sys, requests, codecs, time, re, csv, string
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits
from script_template import create_file, logger
start=time.time()

f = create_file('eng-sur_b_WYbpe', 'w', [35, 102, 'Contact', 'Business', 'Business2', 0, 1, 4, 36, 44, 'Foreign', 21, 'Branch', 32, 'Corp', 13, 19, 37, 6])
l = logger('WYbpe')

driver = webdriver.PhantomJS()

#soup = BeautifulSoup(driver.page_source)

#again=soup.find("option")

def main():
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
                                    
            l.info("\"" + "\",\"".join(info) + "\"\n")

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
                                    
            l.info("\"" + "\",\"".join(info) + "\"\n")

            info=[]

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()

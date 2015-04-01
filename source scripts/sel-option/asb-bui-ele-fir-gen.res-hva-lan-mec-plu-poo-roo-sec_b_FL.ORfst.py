#-*- coding: cp1252 -*-
import requests, re, time, codecs, sys

from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits
import time
from script_template import create_file, logger

f = create_file('asb-bui-ele-fir-gen.res-hva-lan-mec-plu-poo-roo-sec_b_FL.ORfst', 'w', ['21', '37', 'Application Date', '32', '78', '19', '13', 'description', 'applicant', 'name', '0', '36', '44', 'nothing', '33', '6', '7', '12', '102'])
l = logger('asb-bui-ele-fir-gen.res-hva-lan-mec-plu-poo-roo-sec_b_FL.ORfst')
driver =webdriver.PhantomJS()

def main():
    driver.get("https://fasttrack.ocfl.net/PublicPortal/OC/SearchContractor.jsp")
    soup = BeautifulSoup(driver.page_source)
    test = soup.findAll("option")

    peach=[]
    for sbe in test:
        peach.append(sbe.text)
    role = 1

    while role == 1:
        try:
            for k in range(1,len(peach)):
                if k == len(peach)+1:
                    break

                else:
                    driver.get("https://fasttrack.ocfl.net/PublicPortal/OC/SearchContractor.jsp")
                    driver.find_elements_by_tag_name("option")[k].click()
                    driver.find_element_by_css_selector("#btnSearch").click()
                    soup = BeautifulSoup(driver.page_source)
                    length = soup.findAll("tr",{"class":"FormtableData1"})
                    length2 = soup.findAll("tr",{"class":"FormtableData2"})
                    apple = []
                    for a in length:
                        apple.append(a.text)
                    for b in length2:
                        apple.append(b.text)

                    l.debug(len(apple))

                    for l in range (0,len(apple)):
                        try:
                            driver.find_elements_by_class_name("alink")[l].click()
                            soup = BeautifulSoup(driver.page_source)
                            info = []                      
                            for mango in soup.findAll('tr',{"class":"FormtableData1"}):
                                for dat in mango.findAll("td"):
                                    info.append(dat.text)
                            try:
                                if len(info[10])>3:                
                                    info[10] = info[10].strip()
                                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                                    info[10] = re.sub("Phone:","",info[10])
                                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                                else:
                                    info[10] = "     "
                                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))              
                            except:
                                pass
                            try:
                                if len(info[11])>1:
                            
                                    info[11] = re.sub(u"Â","",info[11])
                                    info[11] = re.sub("Escrow",'',info[11])
                                    info[11] = re.sub("Company",'1',info[11])
                                    info[11] = re.sub("",' ',info[11])
                                else:
                                    info.append(" ")   
                            except:
                                pass

                            try:
                                info[12] = re.sub("Escrow Deposit","",info[12])
                            except:
                                pass
                            try:
                                info[13:35]=[]
                            except:
                                pass
                            try:
                                if len(info[12])>2:
                                    info.append(info[12])
                                else:
                                    info.append(info[9])
                            except:
                                pass
                            while len(info) < 11:
                                info.append("")
                            info.append("license number")
                                    

                            l.info(info)
                            f.write("|".join(info) + "\n")
              
                            driver.find_element_by_id("back").click()
                        except Exception, e:
                            l.error(str(e))
            role += 1

        except Exception, e:
            l.error(str(e))
            pass

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
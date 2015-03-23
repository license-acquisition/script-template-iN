from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, codecs

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

page = 1
f = codecs.open("fir_b_OHsfm_%s_000.csv"%(time.strftime("%Y%m%d")),"a","utf-8")
f.write("entity_name|license_number|licensee_type_cd|first_issue_date|expiration_date|status|status_reason|company_flag|address1|state|zip|phone|email\n")

driver = webdriver.PhantomJS()

driver.get('https://elicense7.com.ohio.gov/Lookup/LicenseLookup.aspx')
driver.find_element_by_xpath('//*[@id="ctl00_MainContentPlaceHolder_ucLicenseLookup_ctl01_lbMultipleCredentialTypePrefix"]/option[3]').click()

driver.find_element_by_id("btnLookup").click()
time.sleep(3)
page = 1


while page < 10000:
    print (page)
    peach = []
    test = driver.find_elements_by_link_text("Detail")
    for ava in test:
        peach.append(ava.text)

    print len(peach)

    for k in range (0,len(peach)):

        try:


            info = []
            info2 = []
            
            
            driver.find_elements_by_link_text("Detail")[k].click()
            time.sleep(1)
            soup = BeautifulSoup(driver.page_source)

            div = soup.find('div',{'id':'ctl00_MainContentPlaceHolder_ucLicenseDetailPopup_UpdatePanel1'})
            tod = div.findAll('td')

            for col in tod:
                info.append(col.text)

            name = info[0]
            info2.append(name)

            lic_num = info[2]
            info2.append(lic_num)

            lic_type = info[3]
            info2.append(lic_type)

            issue = info[4]
            info2.append(issue)

            exp = info[5]
            info2.append(exp)

            status = info[6]
            info2.append(status)

            statusre = info[7]
            info2.append(statusre)

            info[1]= "\"|\"".join(info[1].rsplit("Email:", 1))
            info[1]= "\"|\"".join(info[1].rsplit("Phone:", 1))
            info[1]= "\"|\"".join(info[1].rsplit("  ", 1))
            info[1]= "\"|\"".join(info[1].rsplit(", ", 1))

            info2.append("1")

            add = info[1]
            info2.append(add)

            print ("\"" + "\",\"".join(info2) + "\"\n")
            f.write("\"" + "\"|\"".join(info2) + "\"\n")

            
     

            hello = driver.find_elements_by_id("ctl00_MainContentPlaceHolder_ucLicenseDetailPopup_linkToCloseLicDet")
            hello[0].click()

            time.sleep(1)

        except Exception, e:
            print str(e)
            continue


    try:

        if page == 10:
            page = page + 1
            driver.find_element_by_xpath("//*[@id='ctl00_MainContentPlaceHolder_ucLicenseLookup_gvSearchResults']/tbody/tr[38]/td/table/tbody/tr/td[11]/a").click()
            time.sleep(2)         
        elif page % 10 != 0:
            page = page + 1
            driver.find_element_by_xpath("(//a[contains(text()," + str(page) + ")])[2]").click()
            time.sleep(2)
        else:
            page = page + 1
            driver.find_element_by_xpath("(//a[contains(text(),'...')])[4]").click()
            time.sleep(2)
            
                

    except Exception, e:

        print str(e)

        continue
f.close()
browser.close()
browser.quit()

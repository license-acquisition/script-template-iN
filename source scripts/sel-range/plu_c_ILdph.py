import sys, csv, re, requests, time, string, codecs 
from bs4 import BeautifulSoup
from selenium import webdriver # Automate browser.
from selenium.webdriver.common.by import By # For waiting for page loads.
from selenium.webdriver.support.ui import WebDriverWait # For waiting for page loads.
from selenium.webdriver.support import expected_conditions as EC # Wait for load.

start = time.time()

f = codecs.open('plu_c_ILdph_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')

headers = ["entity_name", "license_number", "address1", "state", "zip", "licensee_type_cd", "phone", "status", "employer", "expiration_date", "first_issue_date", "ce_hours", "company_flag"]

f.write("|".join(headers) + "\n")

driver = webdriver.PhantomJS()

url = 'https://plumblicv5pub.dph.illinois.gov/Clients/ILDOHPlumb/Public/Verification/Plumber_License_Verification.aspx'

driver.get(url)

for i in range (23840,99999): # originally -> 23840

    info = []

    info2 = []

    driver.get(url)

    idnumber = driver.find_element_by_id("txtLicenseID")

    idnumber.send_keys("055-%06d"%i)
 
    driver.find_element_by_id("btnSearch").click()

    try:

        driver.find_element_by_css_selector('#dtgList > tbody > tr:nth-child(2) > td:nth-child(1) > a').click()

        driver.switch_to_window("_BLANK")

        soup = BeautifulSoup(driver.page_source)

        results = soup.find('table', id = 'tblresults')

        columns = results.findAll('td')

        for col in columns:
            info.append(col.text)

        info[7] = info[7] = "\",\"".join(info[7].rsplit(", ", 1))
        info[7] = info[7] = "\",\"".join(info[7].rsplit(" ", 1))
                        

        info2.append(info[3])
        info2.append(info[5])
        info2.append(info[7])
        info2.append(info[9])
        info2.append(info[11])
        info2.append(info[13])
        info2.append(info[15])
        info2.append(info[17])
        info2.append(info[21])
        info2.append(info[25])
        info2.append("1")

        print info2
        f.write("|".join(info2) + "\n")

        

    except Exception, e:

        print str(e)
        print "Move on bugger"
        print i
        continue

final = (time.time() - start)/60.0
f.write('Minutes elapsed: %s' %str(final))
f.close()
driver.close()
        

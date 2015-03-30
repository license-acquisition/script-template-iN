import sys, csv, re, requests, time, string, codecs 
from bs4 import BeautifulSoup
from selenium import webdriver # Automate browser.
from selenium.webdriver.common.by import By # For waiting for page loads.
from selenium.webdriver.support.ui import WebDriverWait # For waiting for page loads.
from selenium.webdriver.support import expected_conditions as EC # Wait for load.
from script_template import create_file, logger

f = create_file('plu_c_ILdph', 'w', ['12', '21', '0', '36', '44', '32', '33', '37', '65', '13', '19', '55', '6'])
l = logger('plu_c_ILdph')
driver = webdriver.PhantomJS()
s = requests.Session()

def main():
    url = 'https://plumblicv5pub.dph.illinois.gov/Clients/ILDOHPlumb/Public/Verification/Plumber_License_Verification.aspx'
    s.get(url)
    driver.get(url)
    for i in range (23840,99999): # originally -> 23840
        info = []
        info2 = []
        driver.get(url)
        idnumber = driver.find_element_by_id("txtLicenseID")
        idnumber.send_keys("055-%06d"%i) 
        driver.find_element_by_id("btnSearch").click()
        try:
            soup = BeautifulSoup(driver.page_source)
            for link in soup.find_all('a'):
                if 'PLUMBER_LICENSE_DETAILS' in link['href']:
                    l.info(link['href'][2:])
                    page = s.get('https://plumblicv5pub.dph.illinois.gov/Clients/ILDOHPlumb/Public/Verification/' + link['href'][2:])
                    soup = BeautifulSoup(page.content)
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

                    l.info(info2)
                    f.write("|".join(info2) + "\n")

        except Exception, e:
            l.error(str(e))
            l.debug("Move on bugger")
            l.debug(i)
            continue

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
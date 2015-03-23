import requests, codecs, time
from bs4 import BeautifulSoup
#<<<<<<< HEAD:Trigger/Source Scripts/HI/gen.res_b_HIdcc.py

#=======
#>>>>>>> ea8ddcced279b00725b0af98257566a05f755d5f:Trigger/Source Scripts/HI/HIdcc.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
licenseTypes = ['PJ', 'EJ', 'EM', 'CT', 'PCFR']
f = codecs.open("gen.res_b_HIdcc_20150224_000.txt", "a", "utf-8")
#headers = ['license_number', 'status2', 'status', 'expiration_date', 'Legal License Name', 'Trade/Professional Name', 'Entity', 'issue_date', 'Class Prefix', 'Special Privilege', 'Restriction', 'Education Code', 'Business Code', 'Conditions & Limitations', 'Business Address']
#f.write('|'.join(headers) + '\n')
#<<<<<<< HEAD:Trigger/Source Scripts/HI/gen.res_b_HIdcc.py
browser = webdriver.Chrome()
for lic in licenseTypes:
        i = 25000 # original i = 1
        while i <= 35000:
                info = []
                browser.get("https://pvl.ehawaii.gov/pvlsearch/info/%s-%s-0"%(lic, str(i)))
                try:
                         element = WebDriverWait(browser, 10).until(
                           EC.presence_of_element_located((By.ID, "collapse1"))
                        )
                finally:
                        pass
                try:
                        soup = BeautifulSoup(browser.page_source)
                        for span in soup.findAll("span"):
                                span.extract()
                        for td in soup.findAll("td"):
                                info.append(td.text.replace("&amp;", "&"))
                        i += 1
                        if len(info)>7:
                                f.write("|".join(info) + "\n")
                                print info
                        else:
                                print i
                except Exception, e:
                        print str(e)
                        i += 1
                        print i
'''
=======
browser = webdriver.Chrome()
i=0
while i < 25000:
        info = []
        try:
                browser.get("https://pvl.ehawaii.gov/pvlsearch/info/PCFR-%s-0"%str(i))
        
                element = WebDriverWait(browser, 10).until(
                   EC.presence_of_element_located((By.ID, "collapse1"))
                )
        except:
                continue
        try:
                soup = BeautifulSoup(browser.page_source)
                for span in soup.findAll("span"):
                        span.extract()
                for td in soup.findAll("td"):
                        info.append(td.text.replace("&amp;", "&"))
                i += 1
                if len(info)>7:
                        f.write("\"" + "\",\"".join(info) + "\"\n")
                        print ("\"" + "\",\"".join(info) + "\"\n")
                else:
                        print i
        except Exception, e:
                print str(e)
                i += 1
'''
f.write('It actually finished.')
f.close()
browser.close()
browser.quit()
#>>>>>>> ea8ddcced279b00725b0af98257566a05f755d5f:Trigger/Source Scripts/HI/HIdcc.py

import codecs
from selenium import webdriver
import codecs, re
from bs4 import BeautifulSoup
from string import ascii_uppercase
import time
browser = webdriver.Chrome()
stamp = time.strftime("%Y%m%d")
from itertools import product
#f = codecs.open("eng-sur_c_WAdol_%s_000.csv"%(stamp),"w","utf-8")
#f.write("entity_name,licensee_type_cd,license_number,status,first_issue_date,issue_date,expiration_date,city,state,zip,address1\n")
keywords = [''.join(i) for i in product(ascii_uppercase, repeat =2)]

l=codecs.open("WA_arc_dol_Links.csv","w","utf-8")

browser.get("http://bls.dor.wa.gov/LicenseSearch/")
for x in keywords:
    try:
        #browser.get("http://bls.dor.wa.gov/LicenseSearch/")
        browser.find_element_by_css_selector("#ddLicType > option:nth-child(17)").click()
        search = browser.find_element_by_css_selector('//*[@id="main_ddLicType"]/option[2]')
        search.send_keys("%s"%x)
        browser.find_element_by_css_selector("#main_btnSearch").click()
        print x
        for a in browser.find_elements_by_css_selector("#main_tblResults > tbody > tr > td > a"):
                info = []
                if "javascript:" not in a.get_attribute('href'):
                        info.append((a.get_attribute('href')))
                        print ("\"" + "\"\n\"".join(info) + "\"\n")
                        l.write("\"" + "\"\n\"".join(info) + "\"\n")
    except Exception, e:
        print str(e)
l.close()

"""

for line in codecs.open("WA_dol_Links.csv","r","utf-8"):
	try:
		quotes = "%s" %line
		link = quotes.replace("\"","")
		print link
		browser.get(link)
		info = []
		soup = BeautifulSoup(browser.page_source.replace("<br>","_"))
		relevant_info = soup.findAll("td",{"class":"DefaultTextGV"})
		info.append(relevant_info[0].text)
		info.append(relevant_info[1].text)
		info.append(relevant_info[2].text)
		info.append(relevant_info[3].text)
		info.append(relevant_info[4].text)
		info.append(relevant_info[5].text)
		info.append(relevant_info[6].text)
		\"""for ok in text:
			print re.sub("\n\s*","_",ok.text)""\"
		address = soup.find("table",{"id":"gvAddr1"}).findAll("td",{"class":"DefaultText"})[0].text
		#fulladdress = ok.findAll("td",{"class":"DefaultText"})[0]
		#citystatezip = str(address).split("_"))
		#info.append(citystatezip)
		info.append(str(address))
		print ("\"" + "\"|\"".join(info) + "\"\n")
		f.write("\"" + "\"|\"".join(info) + "\"\n")
	except Exception, e:
		print str(e)
"""
f.close()
browser.close()
browser.quit()

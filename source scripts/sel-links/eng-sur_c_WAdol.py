import codecs
from selenium import webdriver
import codecs, re
from bs4 import BeautifulSoup
from string import ascii_uppercase
import time
from itertools import product
from script_template import create_file, logger

f = create_file('eng-sur_c_WAdol', 'w', ['12', '32', '21', '37', '19', 'issue_date', '13', '4', '36', '44', '0'])
l = logger('eng-sur_c_WAdol')
g = codecs.open('eng-sur_c_WAdol_links.csv', 'w', 'utf-8')
driver = webdriver.PhantomJS()

def main():
	keywords = [''.join(i) for i in product(ascii_uppercase, repeat =2)]
	driver.get("http://bls.dor.wa.gov/LicenseSearch/")
	for x in keywords:
	    try:
	        #driver.get("http://bls.dor.wa.gov/LicenseSearch/")
	        driver.find_element_by_css_selector("#ddLicType > option:nth-child(17)").click()
	        search = driver.find_element_by_css_selector('//*[@id="main_ddLicType"]/option[2]')
	        search.send_keys("%s"%x)
	        driver.find_element_by_css_selector("#main_btnSearch").click()
	        l.info(x)
	        for a in driver.find_elements_by_css_selector("#main_tblResults > tbody > tr > td > a"):
	                info = []
	                if "javascript:" not in a.get_attribute('href'):
	                        info.append((a.get_attribute('href')))
	                        l.info(info)
	                        g.write(info + '\n')
	    except Exception, e:
	        l.error(str(e))
	g.close()

	for line in codecs.open("eng-sur_c_WAdol_links.csv","r"):
		try:
			quotes = "%s" %line
			link = quotes.replace("\"","")
			l.info(link)
			driver.get(link)
			info = []
			soup = BeautifulSoup(driver.page_source.replace("<br>","_"))
			tds = soup.findAll("td",{"class":"DefaultTextGV"})
			info.append(tds[0].text)
			info.append(tds[1].text)
			info.append(tds[2].text)
			info.append(tds[3].text)
			info.append(tds[4].text)
			info.append(tds[5].text)
			info.append(tds[6].text)
			address = soup.find("table",{"id":"gvAddr1"}).findAll("td",{"class":"DefaultText"})[0].text
			info.append(str(address))
			l.info(info)
			f.write("\"" + "\"|\"".join(info) + "\"\n")
		except Exception, e:
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
from selenium import webdriver
from bs4 import BeautifulSoup
import time, re, codecs
from datetime import date
import re
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open("sur_c_TXbls_%s%s%s_0000.csv" %(str(year), str(month).zfill(2), str(day).zfill(2)),"a","utf-8")
browser = webdriver.Chrome()
#f = codecs.open("sur_c_TXbls_20140827_000.csv","a")
f.write("company_flag|registration_flag|number_type|license_number|entity_name|license_type_cd|status,expiration_date|first_renew_date|phone|dba|address1|city|state|county|zip|licensee_role|related_party_role,qualifying_individual|related party role|indiv_address|indiv_address|indiv_zip|cleanhead|cleanhead|cleanhead|cleanhead\n")
browser.get("https://licensing.hpc.state.tx.us/datamart/mainMenu.do")
browser.find_element_by_link_text("Public License Search").click()
#browser.get("https://licensing.hpc.state.tx.us/datamart/selLicType.do?type=county")
browser.find_element_by_link_text("Search by County").click()
browser.find_element_by_css_selector("#licenseType > option:nth-child(12)").click()
browser.find_element_by_css_selector("#contentBox > form > table:nth-child(3) > tbody > tr:nth-child(2) > td > div > div > input:nth-child(1)").click()
browser.find_element_by_css_selector("#rowsPerPage > option:nth-child(4)").click()
x = 346
while x < 3266:
	#county = browser.find_element_by_css_selector("#county > option:nth-child(%d)"%x)
	county = browser.find_element_by_xpath("//*[@id='county']/option[%d]"%x)
	county.click()
	browser.find_element_by_css_selector("#contentBox > form > table:nth-child(2) > tbody > tr:nth-child(2) > td > div > div > input:nth-child(1)").click()
	#soup = BeautifulSoup(browser.page_source)
	try:
		list_of_links = []
		links = browser.find_elements_by_xpath("//*[@id='contentBox']/form/table[2]/tbody/tr/td[1]/span/a")
		for licnumb in links:
			list_of_links.append(licnumb.text)
		print list_of_links, x
		for license in list_of_links:
			browser.find_element_by_link_text(license).click()
			time.sleep(3)
			soup = BeautifulSoup(browser.page_source)
			td = soup.findAll("td",{"class":"dataView"})
			item = soup.findAll("td",{"class":"itemCell"})
			info = []
			info.append("1")
			info.append("Registration")
			for content in td:
				info.append(re.sub("\n\s*"," ",content.text.replace(u'\xa0',u' ')))
			for address in item:
				info.append(re.sub("\n\s*"," ",address.text.replace(u'\xa0',u' ')))
			print ("|".join(info) + "\n")
			f.write("|".join(info) + "\n")
			browser.back()
			time.sleep(2)
		browser.back()
		time.sleep(2)
		x = x + 1
	except Exception, e:
		print str(e)
		browser.back()
		x = x + 1
f.close()
browser.close()
browser.quit()

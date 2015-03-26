from selenium import webdriver
from bs4 import BeautifulSoup
import re, time
from datetime import date
from script_template import create_file, logger
f = create_file("sur_c_TXbls","w",[6,100,102,21,12,32,37,13,20,33,10,0,4,36,8,44,"licensee_role","related_party_role",35,"related_party_role:","indiv_address","indiv_address","cleanhead"])
l = logger("TXbls")


driver = webdriver.PhantomJS()

def main():
	driver.get("https://licensing.hpc.state.tx.us/datamart/mainMenu.do")
	driver.find_element_by_link_text("Public License Search").click()
	#driver.get("https://licensing.hpc.state.tx.us/datamart/selLicType.do?type=county")
	driver.find_element_by_link_text("Search by County").click()
	driver.find_element_by_css_selector("#licenseType > option:nth-child(12)").click()
	driver.find_element_by_css_selector("#contentBox > form > table:nth-child(3) > tbody > tr:nth-child(2) > td > div > div > input:nth-child(1)").click()
	driver.find_element_by_css_selector("#rowsPerPage > option:nth-child(4)").click()
	x = 346
	while x < 3266:
		#county = driver.find_element_by_css_selector("#county > option:nth-child(%d)"%x)
		county = driver.find_element_by_xpath("//*[@id='county']/option[%d]"%x)
		county.click()
		driver.find_element_by_css_selector("#contentBox > form > table:nth-child(2) > tbody > tr:nth-child(2) > td > div > div > input:nth-child(1)").click()
		#soup = BeautifulSoup(driver.page_source)
		try:
			list_of_links = []
			links = driver.find_elements_by_xpath("//*[@id='contentBox']/form/table[2]/tbody/tr/td[1]/span/a")
			for licnumb in links:
				list_of_links.append(licnumb.text)
			for license in list_of_links:
				driver.find_element_by_link_text(license).click()
				time.sleep(3)
				soup = BeautifulSoup(driver.page_source)
				td = soup.findAll("td",{"class":"dataView"})
				item = soup.findAll("td",{"class":"itemCell"})
				info = []
				info.append("1")
				info.append("Registration")
				for content in td:
					info.append(re.sub("\n\s*"," ",content.text.replace(u'\xa0',u' ')))
				for address in item:
					info.append(re.sub("\n\s*"," ",address.text.replace(u'\xa0',u' ')))
				l.info("|".join(info) + "\n")
				f.write("|".join(info) + "\n")
				driver.back()
				time.sleep(2)
			driver.back()
			time.sleep(2)
			x = x + 1
		except Exception, e:
			l.error(str(e))
			driver.back()
			x = x + 1

if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		l.critical(str(e))
	finally:
		f.close()
		driver.close()
		driver.quit()

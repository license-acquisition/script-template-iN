from selenium import webdriver
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('wel_c_NYdec','w',[7,0,4,36,44,33,21,102,32])
l = logger("NYdec")

driver = webdriver.PhantomJS()

def main():
	for i in xrange(2, 18):
		driver.get("http://www.dec.ny.gov/cfmx/extapps/WaterWell/index.cfm")
		driver.find_element_by_css_selector("input[value='Select County']").click()
		driver.find_element_by_css_selector("#activity_code > option:nth-child(%d)"%i).click()
		driver.find_element_by_css_selector("input[value='Start']").click()
		soup = BeautifulSoup(driver.page_source)
		for tr in soup.find_all("table")[0].find_all("tr")[3:-2]:
			data = []
			for td in tr.find_all("td"):
				data.append(td.text.strip())
			data.append("Registration Number")
			data.append("Water Well Contractor")
			f.write("|".join(data) + "\n")
			l.info('\"' + "\",\"".join(data) + "\"\n")
			data = []
		while True:
			try:
				driver.find_element_by_partial_link_text("Next").click()
				soup = BeautifulSoup(driver.page_source)
				for tr in soup.find_all("table")[0].find_all("tr")[3:-2]:
					data = []
					for td in tr.find_all("td"):
						data.append(td.text.strip())	
					data.append("Registration Number")
					data.append("Water Well Contractor")
					f.write("|".join(data) + "\n")
					l.info('\"' + "\",\"".join(data) + "\"\n")
			except Exception, e:
				
				l.error(str(e))
				break	



if __name__ == "__main__":
	try:
		main()
	except Exception, e:
		l.critical(str(e))
	finally:
		driver.close()
		f.close()
		driver.quit()
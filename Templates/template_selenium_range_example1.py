from selenium import webdriver
from bs4 import BeautifulSoup
from script_template import create_file, logger
f = create_file("wel_c_NYdec","w",[12,0,4,36,44,33,21,"number_type",32])
l = logger('NYdec')
browser = webdriver.PhantomJS()


def main():
	start = 2
	end = 18
	for i in range(start, end):
		browser.get("http://www.dec.ny.gov/cfmx/extapps/WaterWell/index.cfm")
		browser.find_element_by_css_selector("input[value='Select County']").click()
		browser.find_element_by_css_selector("#activity_code > option:nth-child(%d)"%i).click()
		browser.find_element_by_css_selector("input[value='Start']").click()
		while True: #avoid while true if you can. 
			try:
				soup = BeautifulSoup(browser.page_source)
				for tr in soup.find_all("table")[0].find_all("tr")[3:-2]:
					info = []
					for td in tr.find_all("td"):
						info.append(td.text.strip())	
					info.append("Registration Number")
					info.append("Water Well Contractor")
					f.write("|".join(info) + "\n")
					l.info('|'.join(info) + "\n")
					browser.find_element_by_partial_link_text("Next").click()
			except:
				#if next doesn't exist, break the while loop
				break
if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		l.critical(str(e))
	finally:
		browser.quit()
		f.close()

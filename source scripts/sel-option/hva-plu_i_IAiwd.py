from selenium import webdriver
from bs4 import BeautifulSoup
from script_template import create_file, logger
<<<<<<< HEAD:source scripts/sel-option/hva-plu_i_IAiwd.py
f = create_file("hva-plu_i_IAiwd","w",['LAST_NAME','FIRST_NAME','MIDDLE_NAME',21,32,37,19,13,"discipline","individual_flag"])
l = logger('IAiwd')
browser = webdriver.PhantomJS()
=======
>>>>>>> origin/master:source scripts/sel-option/hva-plu_i_IAiwd.py

f = create_file("hva-plu_i_IAiwd","w",['LAST_NAME','FIRST_NAME','MIDDLE_NAME',21,32,37,19,13,"discipline"])
l = logger('hva-plu_i_IAiwd')
driver = webdriver.PhantomJS()

def main():
<<<<<<< HEAD:source scripts/sel-option/hva-plu_i_IAiwd.py
	for i in (6,7,10,12):
		browser.get("https://eservices.iowa.gov/licensediniowa/index.php?pgname=pubsearch")
		browser.find_element_by_css_selector("select[name='profession_lic']> option:nth-child(%d)"%i).click()
		browser.find_element_by_css_selector("input[name='serach_lic']").click()
=======
	start = 6
	end = 12
	for i in range(start, end):
		driver.get("https://eservices.iowa.gov/licensediniowa/index.php?pgname=pubsearch")
		driver.find_element_by_css_selector("select[name='profession_lic']> option:nth-child(%d)"%i).click()
		driver.find_element_by_css_selector("input[name='serach_lic']").click()
>>>>>>> origin/master:source scripts/sel-option/hva-plu_i_IAiwd.py

		while True:
			try:
				soup = BeautifulSoup(driver.page_source)
				for tr in soup.find_all("table")[1].find_all("tr")[1:-1]:
					info = []
					for td in tr.find_all("td"):
						info.append(td.text.strip())
						info.append("1")
					f.write("|".join(info) + "\n")
					l.info('|'.join(info) + "\n")
				driver.find_element_by_partial_link_text("Next").click()
			except Exception, e:
				l.error(str(e))
				#if next doesn't exist, break the while loop
				break
				
if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		l.critical(str(e))
	finally:
		driver.quit()
		f.close()

from selenium import webdriver
from bs4 import BeautifulSoup
from script_template import create_file, logger
f = create_file("eng-sur_b_IAiwd","w",[12,7,0,1,4,36,44,33,66,21,32,37,13,19,"METHOD"])
l = logger('IAiwd')
browser = webdriver.PhantomJS()


def main():
	start = 1511
	end = 30000
	for j in range(start,end):
		browser.get("https://eservices.iowa.gov/licensediniowa/index.php?pgname=pubsearch")
		browser.find_element_by_css_selector("select[name='profession_lic']> option:nth-child(5)").click()
		search = browser.find_element_by_css_selector("input[name='licnum']")
		search.send_keys("%05d"%j)
		browser.find_element_by_css_selector("input[name='serach_lic']").click()
		
		while True: #avoid while true if you can. 
			try:
				browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(2) > td > a").click()	
				info = []
				soup = BeautifulSoup(browser.page_source)
				for entity_name in soup.find_all("table")[1].find_all("tr")[1].find_all("td"):
					info.append(entity_name.text.strip())
		
				for contact_info in soup.find_all("table")[2].find_all("tr")[1:]:
					for td in contact_info.find_all("td"):
						if td == "&nbsp":
							pass
						
						else:
							info.append(td.text.strip())
							break

				for license_info in soup.find_all("table")[3].find_all("tr"):
					for td in license_info.find_all("td"):
						if td == "&nbsp":
							pass
						else:
							info.append(td.text.strip())
							break
					
				info = [x for x in info if len(x) !=0]	
				f.write("|".join(info) + "\n")
				print info
				l.info('|'.join(info) + "\n")

			except Exception, e:
				l.error(str(e))
				break
if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		l.critical(str(e))
	finally:
		browser.quit()
		f.close()

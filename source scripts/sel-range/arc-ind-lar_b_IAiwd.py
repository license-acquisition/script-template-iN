from selenium import webdriver
from bs4 import BeautifulSoup
from script_template import create_file, logger
f = create_file("arc-ind-lar_b_IAiwd","w",[12,0,1,"City State Zip",33,66,21,6,37,19,"Discipline","Licensed_By"])
l = logger('IAiwd')
browser = webdriver.PhantomJS()

def main():
	#2,4,5 refers to the tables nested within the parent table that we want. #3 is not necessary.
	table_index_list = [2,4,5]

	#4,8,9 refers to architects, interior desingers, and landscape architects
	for i in (4,8,9):
		start = 1
		end = 30000
		for j in range(start,end):
			browser.get("https://eservices.iowa.gov/licensediniowa/index.php?pgname=pubsearch")
			browser.find_element_by_css_selector("select[name='profession_lic']> option:nth-child(%d)"%i).click()
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
			
					for table_index in table_index_list:
						for license_info in soup.find_all("table")[table_index].find_all("tr"):
							for td in license_info.find_all("td"):
								if td.has_attr("class"):
									continue
								else:
									info.append(td.text.strip())

					#indices refer to the blank spaces within td's that we want to strip out of our final output
					indices = 1,2,3,7,8,9,10,11,17
					info = [a for b, a in enumerate(info) if b not in indices]

					f.write("|".join(info) + "\n")
					#print info
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

from selenium import webdriver
from bs4 import BeautifulSoup
from script_template import create_file, logger
f = create_file("arc-ind-lar_b_IAiwd","w",[12,0,1,4,36,44,33,66,21,7,37,13,19,"licensed_by"])
l = logger('IAiwd')
browser = webdriver.PhantomJS()

def main():
	# remove_list is to substitute empty spaces that should have information with no_info
	remove_list = [1,11,12] 

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
			
					for contact_info in soup.find_all("table")[2].find_all("tr")[1:]:
						for td in contact_info.find_all("td"):
							if td.has_attr("class"):
								continue
							else:
								info.append(td.text.strip())
								

					for license_info in soup.find_all("table")[4].find_all("tr"):
						for td in license_info.find_all("td"):
							if td.has_attr("class"):
								continue
							else:
								info.append(td.text.strip()) 
								

					for issue_info in soup.find_all("table")[5].find_all("tr"):
						for td in issue_info.find_all("td"):
							if td.has_attr("class"):
								continue
							else:
								info.append(td.text.strip())
					for remove in remove_list:
						if info[remove]=="":
							info[remove] = "no_info"	#substitute whitespaces that should have information with no_info to distinguish from below
					info = [x for x in info if len(x) !=0]	#to remove whitespaces that are decoration-only on the site
					for k in range(1,len(info)):
						if "Firm" in info[k]:
							info[i]="1"
						elif "Individual" in info[k]:
							info[i]="0"

					for index in range(0,len(info)):
						if info[index] == "no_info":
							info[index] = ""


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

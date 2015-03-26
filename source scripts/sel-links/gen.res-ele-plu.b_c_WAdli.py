import codecs
from selenium import webdriver
from bs4 import BeautifulSoup
from string import ascii_uppercase
import time
from itertools import product
from script_template import create_file, logger

f = create_file('')

keywords = [''.join(i) for i in product(ascii_uppercase, repeat=3)]
f=codecs.open("WA_dli_links2.csv","a","utf-8")
driver = webdriver.PhantomJS()
driver.implicitly_wait(20)
driver.get("https://secure.lni.wa.gov/verify/Results.aspx#%7B%22firstSearch%22%3A0%2C%22searchCat%22%3A%22Name%22%2C%22searchText%22%3A%22abc%22%2C%22Name%22%3A%22abc%22%2C%22pageNumber%22%3A0%2C%22SearchType%22%3A2%2C%22SortColumn%22%3A%22Rank%22%2C%22SortOrder%22%3A%22desc%22%2C%22pageSize%22%3A100%2C%22ContractorTypeFilter%22%3A%5B%5D%2C%22SessionID%22%3A%221eumgf3an33tcjd1nix55js0%22%2C%22SAW%22%3A%22%22%7D")
urls = set()
for i in range(0, 17576):
	try:
		#driver.get("https://secure.lni.wa.gov/verify/Results.aspx#%7B%22firstSearch%22%3A0%2C%22searchCat%22%3A%22Name%22%2C%22searchText%22%3A%22abc%22%2C%22Name%22%3A%22abc%22%2C%22pageNumber%22%3A0%2C%22SearchType%22%3A2%2C%22SortColumn%22%3A%22Rank%22%2C%22SortOrder%22%3A%22desc%22%2C%22pageSize%22%3A100%2C%22ContractorTypeFilter%22%3A%5B%5D%2C%22SessionID%22%3A%221eumgf3an33tcjd1nix55js0%22%2C%22SAW%22%3A%22%22%7D")
		#driver.get("https://secure.lni.wa.gov/verify/default.aspx")
		driver.find_element_by_css_selector("#txtSearchBy").send_keys("%s"%keywords[i])
		driver.find_element_by_css_selector("#searchButton").click()
		time.sleep(3)
		driver.find_element_by_css_selector("#onlyTrades").click()
		time.sleep(3)
		total = int(driver.find_element_by_id('itemsTotal').text)
		if total > 10:
			driver.find_element_by_css_selector("#resultsLengthSelect > option:nth-child(5)").click()
			time.sleep(5)
		soup = BeautifulSoup(driver.page_source)
	
		print total, keywords[i]
		divs = soup.findAll("div",{"class":"resultItem"})
		info = []
		for div in divs:
			url = div['id']
			print url in urls
			if url not in urls:
				info.append(url)
				urls.add(url)
		if total > 100:
			i = total/100
			x = 0
			while x < i:
				next_button = driver.find_element_by_css_selector("#pagination > span:nth-child(1) > input.nextButton")

				next_button.click()
				time.sleep(3)
				soup = BeautifulSoup(driver.page_source)
				divs = soup.findAll("div",{"class":"resultItem"})
				for div in divs:	
					url = div['id']
					print url in urls
					if url not in urls:
						info.append(url)
						urls.add(url)
				x = x+1
		# print ("\"" + "\"\n\"".join(info) + "\"\n")
		print 'appending to list'
		f.write("\"" + "\"\n\"".join(info) + "\"\n")
	except Exception, e:
		print str(e)

#driver.find_element_by_css_selector("#pagination > span:nth-child(3) > input.nextButton").click()
f.close()
driver.close()
driver.quit()

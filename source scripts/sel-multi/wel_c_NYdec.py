import codecs, re, csv, time
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
start=time.time()
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open('wel_c_NYdec_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')
f.write("company_flag|address1|city|state|zip|phone|license_number|number_type|licensee_type_cd\n")

browser = webdriver.PhantomJS()

for i in xrange(2, 18):
	browser.get("http://www.dec.ny.gov/cfmx/extapps/WaterWell/index.cfm")
	browser.find_element_by_css_selector("input[value='Select County']").click()
	browser.find_element_by_css_selector("#activity_code > option:nth-child(%d)"%i).click()
	browser.find_element_by_css_selector("input[value='Start']").click()
	soup = BeautifulSoup(browser.page_source)
	for tr in soup.find_all("table")[0].find_all("tr")[3:-2]:
		data = []
		for td in tr.find_all("td"):
			data.append(td.text.strip())
		data.append("Registration Number")
		data.append("Water Well Contractor")
		f.write("|".join(data) + "\n")
		print('\"' + "\",\"".join(data) + "\"\n")
		data = []
	while True:
		try:
			browser.find_element_by_partial_link_text("Next").click()
			soup = BeautifulSoup(browser.page_source)
			for tr in soup.find_all("table")[0].find_all("tr")[3:-2]:
				data = []
				for td in tr.find_all("td"):
					data.append(td.text.strip())	
				data.append("Registration Number")
				data.append("Water Well Contractor")
				f.write("|".join(data) + "\n")
				print('\"' + "\",\"".join(data) + "\"\n")
		except:
			#print "EXCEPTION"
			break	
print time.time()-start	

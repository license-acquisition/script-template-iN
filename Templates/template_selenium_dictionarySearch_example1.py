import requests, codecs, time
from string import ascii_lowercase
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import product
from selenium.webdriver.support import expected_conditions as EC

def main():
	#standardized code
	time_stamp = time.strftime("%Y%m%d")
	#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
	f = codecs.open("gen.res_c_MDllr_%s_000.txt" % time_stamp, "w","UTF-8")
	headers = ["entity_name","address1","city","state","zip","expiration_date","license_type_cd","suffix"] #always use canonical headers
	f.write("|".join(headers) + "\n")
	#dictionary search list. change what the repeat equals depending on the website requirements
	keywords = [''.join(i) for i in product(ascii_lowercase, repeat=3)]
	driver = webdriver.Chrome()
	driver.implicitly_wait(10)

	try:
		#loose script logic
		for lictype in ['LA','LS']:
			url = 'https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=%s::%s_business_name' %(lictype, lictype)
			
			for keyword in keywords: #alternatively use i in range(0,len(keywords)) keywords[i]
				print "Searching %s %s" % (lictype,keyword)
				driver.get(url)
				driver.find_element_by_css_selector("input[name=businessname]").send_keys("%s" % keyword)
				driver.find_element_by_css_selector("input[name=Submit]").click()
				soup = BeautifulSoup(driver.page_source)
				try:
					while True:
						for tr in soup.find("table",{"border":"4"}).find_all("tr")[1:]:
							info = []
							for td in tr.find_all("td"):
								info.append(td.text.strip())
							print info
							f.write("|".join(info).replace("&amp;","&") + "\n")
						driver.find_element_by_css_selector("input[value=' Next 50 ']").click()
				except:
					pass
				'''parse the page source in any way you need to, then write to file.'''
				#driver.back() may be neccessary 
	except Exception, e:
		print str(e)
	finally:
		driver.close()
		driver.quit()
		f.close()

if __name__ == '__main__':
	main()


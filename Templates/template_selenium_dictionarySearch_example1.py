import requests
from string import ascii_lowercase
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import product
from script_template import create_file

f = create_file("gen.res_c_MDllr", "w", [12, 0, 4, 36, 44, 13, 32, "suffix"])
driver = webdriver.PhantomJS()
driver.implicitly_wait(10)
def main():
	#standardized code
	#dictionary search list. change what the repeat equals depending on the website requirements
	keywords = [''.join(i) for i in product(ascii_lowercase, repeat=3)]
	

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
			except Exception, e:
				print str(e)
			'''parse the page source in any way you need to, then write to file.'''
			#driver.back() may be neccessary



if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		print str(e)
	finally:
		driver.close()
		driver.quit()
		f.close()


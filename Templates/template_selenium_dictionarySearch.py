import requests, codecs, time
from string import ascii_lowercase
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import product

def main():
	#standardized code
	#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
	f = codecs.open("type_entityType_authority_%s_000.csv" % time.strftime("%Y%m%d"), "w","UTF-8")
	headers = ["canonical_name","canonical_name","..."] #always use canonical headers
	f.write("|".join(headers) + "\n")
	#dictionary search list. change what the repeat equals depending on the website requirements
	keywords = [''.join(i) for i in product(ascii_lowercase, repeat=3)]
	driver = webdriver.chrome()
	driver.implicitly_wait(10)
	#end standardized code

	try:
		#loose script logic
		for keyword in keywords: #alternatively use i in range(0,len(keywords)) keywords[i]
			driver.find_element_by_css_selector("#searchbox").send_keys("%s" % keyword)
			driver.find_element_by_css_selector("#searchbutton").click()
			soup = BeautifulSoup(driver.page_source)
			info = {}
			'''

				parse the page source in any way you need to, then write to file.


			'''
			f.write("|".join(info) + "\n")
			#driver.back() may be neccessary 
	except Exception, e:
		print str(e)
	finally:
		driver.close()
		driver.quit()
		f.close()

if __name__ == '__main__':
	main()


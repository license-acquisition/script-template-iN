import requests, codecs, time
from string import ascii_lowercase
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import product
from script_template import create_file, logger

def main():

	#start standardized code
        
	#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
	f = create_file("type_entityType_authority", "w", [headers array]) #reference canonical headers doc
	
	#dictionary search list. change what the repeat equals depending on the website requirements
	keywords = [''.join(i) for i in product(ascii_lowercase, repeat=3)]
	
        driver = webdriver.chrome()

	driver.implicitly_wait(10)

	#end standardized code

	try:

                logger(f.name, 'START')
                
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
		logger(f.name, 'COMPLETE')
	except Exception, e:
		print str(e)
		logger(f.name, 'ERROR', 'explanation') # <- here it would be helpful to log the last keyword searched before error
	finally:
		driver.close()
		driver.quit()
		f.close()

if __name__ == '__main__':
	main()


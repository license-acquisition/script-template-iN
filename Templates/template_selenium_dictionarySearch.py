from string import ascii_lowercase
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import product
from script_template import create_file

#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
#reference canonical headers doc
f = create_file("type_entityType_authority", "w", [header1,header2,...])
driver = webdriver.Chrome()
driver.implicitly_wait(10)

def main():

	#start standardized code
        
	
	
	#dictionary search list. change what the repeat equals depending on the website requirements
	keywords = [''.join(i) for i in product(ascii_lowercase, repeat=3)]
	

	#end standardized code

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


if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		print str(e)
	finally:
		driver.close()
		driver.quit()
		f.close()


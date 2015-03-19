from selenium import webdriver
from bs4 import BeautifulSoup
from script_template import create_file

#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
f = create_file('pro-type_entity-type_authority','w',[header_num, header_num,...])
browser = webdriver.PhantomJS() #use phantom js when available

def main():
	#### standardized code
	#always use canonical headers

	start = 0
	end = 0
	for i in range(start, end):
		#general application logic
		url = "example.com\licenses%d" % i
		browser.get(url)
		soup = browser.page_source
		info = []
		f.write("|".join(info) + "\n")


if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		print str(e)
	finally:
		browser.close()
		browser.quit()
		f.close()
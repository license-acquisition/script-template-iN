import codecs, csv, time
from selenium import webdriver
from bs4 import BeautifulSoup

def main():
	#### standardized code
	time_stamp = time.strftime("%Y%m%d")
	#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
	f = codecs.open("type_entity_type_authority_%s_000.csv" % time_stamp, "w","UTF-8")
	headers = ["canonical_name","canonical_name","..."] #always use canonical headers
	f.write("|".join(headers) + "\n")
	browser = webdriver.PhantomJS() #use phantomjs when available
	#wrap all parsing logic in try finally block, ensures browser closure etc.
	try:
		start = 0
		end = 0
		for i in range(start, end):
			#general application logic
			url = "example.com\licenses%d" % i
			browser.get(url)
			soup = browser.page_source
			info = []
			f.write("|".join(info) + "\n")
	except Exception, e:
		print str(e)
	finally:	
		browser.close()
		browser.quit()
		f.close()

if __name__ == '__main__':
	main()
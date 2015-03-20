import requests#optional: re, string
from bs4 import BeautifulSoup
from script_template import create_file

f = create_file('pro-type_entity-type_authority','w',[header_num, header_num,...])
l = logger('authority')

def main():
	#######this should be standard
	url = "www.example.com/licenses"
	page = requests.get(url)
	soup = BeautifulSoup(page.content)
	# End of standardized section

	#parsing logic. interact with soup object, create loops, etc.
	info = []
	f.write("|".join(info) + "\n")
	
	#end of parsing logic

if __name__ == "__main__":
	try:
		main()
		l.info('complete')
	except Exception, e:
		l.critical(str(e)) # all critical logs will write to main log
	finally:
		f.close()

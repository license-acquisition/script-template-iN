import requests#optional: re, string
from bs4 import BeautifulSoup
from script_template import create_file

f = create_file('pro-type_entity-type_authority','w',[header_num, header_num,...])
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
	except Exception, e:
		print str(e)
	finally:
		f.close()
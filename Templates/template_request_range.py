import requests #optional: re, string
from bs4 import BeautifulSoup
from script_template import create_file

#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
f = create_file('pro-type_entity-type_authority','w',[header_num, header_num,...])


def main():
	#### standardized code
	start = 0 #change start and end
	end = 0
	###application logic
	for i in range(start, end):
		url = "www.example.com/license_name%d" % i
		page = requests.get(url)
		soup = BeautifulSoup(page.content)
		info = []				
		f.write("|".join(info) + "\n")
		

if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		print str(e)
	finally:
		f.close()
import csv, codecs, requests, time #optional: re, string
from bs4 import BeautifulSoup

def main():
	#### standardized code
	#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
	f = codecs.open("type_entity_type_authority_%s_000.csv" % time.strftime("%Y%m%d"), "w","UTF-8")
	
	headers = ["canonical_name","canonical_name","..."] #always use canonical headers
	f.write("|".join(headers) + "\n")
	

	start = 0 #change start and end
	end = 0
	###application logic
	try:
		for i in range(start, end):
			try:
				url = "www.example.com/license_name%d" % i
				page = requests.get(url)
				soup = BeautifulSoup(page.content)
				info = []


				
				f.write("|".join(info) + "\n")
			except Exception, e:
				print str(e)
				#optional: add other things to do when you fail
	except Exception, e:
		print str(e)
	finally:
		f.close()
		

if __name__ == '__main__':
	main()
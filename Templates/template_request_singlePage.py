import csv, requests, time, codecs #optional: re, string
from bs4 import BeautifulSoup

def main():
	#######this should be standard
	time_stamp = time.strftime("%Y%m%d")
	#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
	f = codecs.open("type_entity_type_authority_%s_000.csv" % time_stamp, "w","UTF-8")
	headers = ["canonical_header","canonical_header","..."] #always use canonical headers
	f.write("|".join(headers) + "\n")
	url = "www.example.com/licenses"
	page = requests.get(url)
	soup = BeautifulSoup(page.content)
	# End of standardized section

	#parsing logic. interact with soup object, create loops, etc.
	try:
		info = []
		f.write("|".join(info) + "\n")
	except Exception, e:
		print str(e)
	finally:
		f.close()
	#end of parsing logic

if __name__ == "__main__":
	main()
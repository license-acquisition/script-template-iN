import csv, requests, time, codecs #optional: re, string
from bs4 import BeautifulSoup

def main():
	#######this should be standard
	time_stamp = time.strftime("%Y%m%d")
	#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
	f = codecs.open("led_c_OKsdh_%s_000.csv" % time_stamp, "w","UTF-8")
	headers = ["entity_name","license_number","address1","city","state","zip","phone","fax","license_type_cd","number_type","company_flag"] #always use canonical headers
	f.write("|".join(headers) + "\n")
	url = "http://www.deq.state.ok.us/aqdnew/lbp/Certified%20Lists/CertifiedLBPFirms.html"
	page = requests.get(url)
	soup = BeautifulSoup(page.content)
	# End of standardized section

	#parsing logic. interact with soup object, create loops, etc.
	try:
		for tr in soup.find_all('tr'):
		    info = []
		    for td in tr.find_all('td'):
		        info.append(td.text)
		    info.append('Certified LBP Firms')
		    info.append('Certification Number')
		    info.append('1')
		    if len(info) > 3:
		        f.write("|".join(info) + "\n")
		        print("\"" + "\",\"".join(info) + "\"\n")
	except Exception, e:
		print str(e)
	finally:
		f.close()
	#end of parsing logic


if __name__ == "__main__":
	main()
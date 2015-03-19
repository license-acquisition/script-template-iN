import requests #optional: re, string
from bs4 import BeautifulSoup
from script_template import create_file

f = create_file('led_c_OKsdh','w',[12,0,4,36,44,33,66,32,102,6])

def main():
	#######this should be standard
	url = "http://www.deq.state.ok.us/aqdnew/lbp/Certified%20Lists/CertifiedLBPFirms.html"
	page = requests.get(url)
	soup = BeautifulSoup(page.content)
	# End of standardized section

	#parsing logic. interact with soup object, create loops, etc.
	
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
	
	#end of parsing logic


if __name__ == "__main__":
	try:
		main()
	except Exception, e: 
		print str(e)
	finally:
		f.close()
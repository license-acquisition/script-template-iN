import codecs, re, requests, csv, time, sys
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('wel_c_NDswc', 'w', ['7', '32', '12', '102', '21', '0', '4', '36', '44', '33', '11'])
l = logger('wel_c_NDswc')
s = requests.session()

def main():
	page = s.post("http://www.swc.nd.gov/4dlink2/4dcgi/ContractSearch",
                data={	"webCategory":"ND Water Well Contractors","wCertType":"All","wSEARCHTYPE":"AND", "Button":"Query"})
	soup = BeautifulSoup(page.content)
	Email = False
	i=1
	while True:
		a = soup.find_all("a")[-i]
		url =  a["href"]
		if a.text == "Search Form":
			break
		page = s.get("http://www.swc.nd.gov/%s"%url)
		soup = BeautifulSoup(page.content)
		table = soup.find("table", {"class" : "sitelist"})
		info = []
		for tr in table.find_all("tr")[1:]:
			if "Email" in tr.text:
				Email = True
			for td in tr.find_all("td"):
				info.append(td.text.strip().replace(u',',' '))	
				
			if Email == True:
				for delIndex in [11, 10, 8, 7, 5, 2]:
					del(info[delIndex])
				info[4] = re.sub("\s+", " ", info[4])
				info[4] = "|".join("|".join(info[4].rsplit(" ", 2)).split(",", 1))
				f.write("|".join(info).replace("Certificate No.: ", "Certificate No.|") + "\n")
				l.info(info)
				info = []
				Email = False
		i+=1

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()

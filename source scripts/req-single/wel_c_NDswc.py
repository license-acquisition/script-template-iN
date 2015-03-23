import codecs, re, requests, csv, time, sys
from bs4 import BeautifulSoup
from datetime import date
start=time.time()
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open('wel_c_NDswc_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')
f.write("company_name|licensee_type_cd|entity_name|number_type|license_number|address1|city|state|zip|phone|email\n")
s = requests.session()
page = s.post("http://www.swc.nd.gov/4dlink2/4dcgi/ContractSearch",
data={	"webCategory":"ND Water Well Contractors","wCertType":"All","wSEARCHTYPE":"AND", "Button":"Query"}).content
soup = BeautifulSoup(page)
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
	payload = []
	for tr in table.find_all("tr")[1:]:
		if "Email" in tr.text:
			Email = True
		for td in tr.find_all("td"):
			payload.append(td.text.strip().replace(u',',' '))	
			
		if Email == True:
			for delIndex in [11, 10, 8, 7, 5, 2]:
				del(payload[delIndex])
			payload[4] = re.sub("\s+", " ", payload[4])
			payload[4] = "|".join("|".join(payload[4].rsplit(" ", 2)).split(",", 1))
			f.write("|".join(payload).replace("Certificate No.: ", "Certificate No.|") + "\n")
			print("|".join(payload) + "\n")
			payload = []
			Email = False
	i+=1
print time.time()-start			
f.close()

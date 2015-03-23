import codecs, re, requests, csv, time, sys
from bs4 import BeautifulSoup
from datetime import date
start=time.time()

f = codecs.open('led_c_ILdph_%s_000.csv' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
f.write("licensee_type_cd|number_type|license_number|entity_name|last update|county|address1|city|state|zip|expiration_date|phone|fax\n")
s = requests.session()
found = True
try:
	for i in xrange(1,999999999,20):
		if found == False:
			break
		found = False
		url = "http://app.idph.state.il.us/envhealth/lead/LeadListing.asp?list=contractors&NoRec=20&Go=Go"
		page = s.get(url)
		page = s.get("http://app.idph.state.il.us/envhealth/lead/genericdb/code/GenericList.asp?START=" + str(i))
		soup = BeautifulSoup(page.content)

		for link in soup.find_all("a"):
				try:
					if 'GenericView' in link['href']:
						found = True
						soup= BeautifulSoup(s.get("http://app.idph.state.il.us" + link["href"]).content)
						#print soup.text
						data = []
						data.append("Licensed Lead Contractors")
						data.append("License Number")
						table = soup.find_all("table", {"cellpadding" : "2"})[1]
						for tr in table.find_all("tr"):
							data.append(re.sub("\s+", " ", tr.find_all("td")[1].text.strip().replace(u',',' ')))
							#for td in tr.find_all("td", {"bgcolor" : "White"}):
							#	data.append(td.text)
						print("\"" + "\",\"".join(data) + "\"\n")
						f.write("|".join(data) + "\n")
				except Exception as e:
					print data
					print str(e)
					pass
except Exception as e:
	print str(e)

print time.time()-start	

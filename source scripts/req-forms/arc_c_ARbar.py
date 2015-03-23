import codecs, re, requests, csv, time
from bs4 import BeautifulSoup
from datetime import date
start=time.time()
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open('arc_c_ARbar_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')
f.write("license_number, company_flag, address1, city, state, zip, status, expiration_date, number_type, licensee_type_cd\n")

url = "https://www.ark.org/asbalaid/index.php/arch/search_firm"
page = requests.get(url)
soup = BeautifulSoup(page.content)

i=0
for option in soup.find("select", {"name" : "state"}).find_all("option")[1:]:
	urlnext = "https://www.ark.org/asbalaid/index.php/arch/search_firm?license_num=&name=&city=&state=" + option['value'] + "&submit=Search%21" 
	pagenext = requests.get(urlnext)
	soupnext = BeautifulSoup(pagenext.content)
	for link in soupnext.find_all("a"):
		try:
			if 'details' in link['href']:
				pagelast = requests.get(link["href"])
				souplast = BeautifulSoup(pagelast.content)
				data = []
				for tr in souplast.find("table", {"class" : "table"}, {"width" : "75%"}).find_all("tr"):
					for td in tr.find_all("td")[1:]:
						data.append(td.text)
				data.append(souplast.find_all("div", {"class" : "row-fluid"}, {"align" : "center"})[1].find("strong").text)
				for link in souplast.find_all("a"):
					try:
						if 'certificate_firm' in link['href']:
							pagecert = requests.get(link['href'])
							soupcert = BeautifulSoup(pagecert.content)
							data.append(soupcert.find_all("p", {"align" : "center"})[0].find("strong").text.replace("This individual registration expires on ", ""))
					except Exception, e:
						print str(e)
				print len(data)
				while len(data) < 8:
					data.append("")
				data.append("Certificate of Authorization Number")
				data.append("Architectural Firm")								
				f.write('\"' + "\",\"".join(data) + "\"\n")
				print ('\"' + '\"\n\"'.join(data))
		except Exception, e:
			print str(e)
	i=i+1		
print time.time()-start			

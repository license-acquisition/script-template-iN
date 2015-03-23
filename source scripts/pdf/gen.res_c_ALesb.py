import requests, re, codecs, time
from subprocess import call
from bs4 import BeautifulSoup
from datetime import date

start = time.time()

soup = BeautifulSoup(requests.get("http://www.aesbl.alabama.gov/licensees.aspx").content)
links = [a.attrs.get('href') for a in soup.select('#form1 > div.main > div.content_container > div > a')]
url = "http://www.aesbl.alabama.gov/" + str(links[0])
print links[0]
print url
pdfFile = open("gen.res_c_ALesb.pdf", "w")
pdfFile.write(requests.get(url).content)
pdfFile.close()
call(["pdftotext", "-layout", "-table", "gen.res_c_ALesb.pdf"], shell=True)

f = codecs.open('gen.res_c_ALesb_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
f.write("|".join(["license_number","license_name","license_type","address1","city","state","zip","licensee_name","phone"]) + "\n")

for line in open("gen.res_c_ALesb.txt", "r"):
	nline = re.sub("   *", "_%_", line)
	nline = re.sub("\n", "", nline)
	nline = nline.split("_%_")
	if len(nline) > 7:
		f.write("|".join(nline) + "\n")
f.close()

print time.time()-start

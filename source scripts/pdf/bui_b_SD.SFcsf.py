from subprocess import call
import re
import requests
from bs4 import BeautifulSoup
import codecs
from datetime import date
import codecs, time
start = time.time()
year = date.today().year
month = date.today().month
day = date.today().day

"""s = requests.session()
sourceurl = "http://www.siouxfalls.org/planning-building/building/plumbing.aspx"
sourcepage = s.get(sourceurl)
soup = BeautifulSoup(sourcepage.content)
print soup.prettify()
for a in soup.findAll("a"):
	if "pdf" in soup.findAll("a"):
		link = []
		link.append(a['href'])
		print link"""

#
#http://www.siouxfalls.org/planning-building/building/electrical.aspx
#http://www.siouxfalls.org/planning-building/building/building.aspx
#http://www.siouxfalls.org/planning-building/building/mechanical.aspx
mcl = "http://www.siouxfalls.org/~/media/Documents/building/2014/MCL_4-17-14.pdf"
rbc = "http://www.siouxfalls.org/~/media/Documents/building/2014/RBC_list-7-3-14.pdf"

f = codecs.open("ele_b_SD.SFcsf_%s%s%s_000.csv" %(str(year), str(month).zfill(2), str(day).zfill(2)),"w","utf-8")
open("well.pdf", "w").write(requests.get("http://www.siouxfalls.org/~/media/Documents/building/2014/RBC_list-7-3-14.pdf").content)
call(["pdftotext", "-layout", "well.pdf"])
f.write("license_type_cd,license_number,entity_name,address1,city,state,zip,phone,phone_cat,qualifying_individual,number_type,company_flag\n")

for line in open("well.txt", "r"):
	nline = re.sub("   *", "_%_", line)
	nline = re.sub("\n", "", nline)
	nline = nline.split("_%_")
	nline.append("License")
	nline.append("1")
	if len(nline) == 11:
		nline[6] = (nline[6] + nline[7])
		state = nline[4].split(",")[1]
		nline[4] = nline[4].split(",")[0]
		nline.insert(5,state)
		print("\"" + "\",\"".join(nline) + "\"\n")
		f.write("\"" + "\",\"".join(nline) + "\"\n")

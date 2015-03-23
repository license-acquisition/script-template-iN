#download AsbestosConsultantAgencies.pdf at:
# http://www.dshs.state.tx.us/WorkArea/linkit.aspx?LinkIdentifier=id&ItemID=54848
import requests, re, codecs, time
from bs4 import BeautifulSoup
from subprocess import call

#call(["pdftotext","-layout -table","AsbestosConsultantAgencies.pdf"],shell = True)

f = open("asb_c_TXdhs_%s_000.csv"%time.strftime("%Y%m%d"),"w")

headers = ['file_number','license_number','entity_name','address1','city','state','zip','county','phone','expiration_date','status','issue_date','rank_date']

f.write("|".join(headers)+"\n")
for line in open("AsbestosConsultantAgencies.txt","r"):
	if "Phone" not in line:
		nline = re.sub("   *","_%_", line)
		nline = re.sub("\n", "", nline)
		nline = nline.split("_%_")
		if len(nline) > 10:
			f.write("|".join(nline) + "\n")
f.close()
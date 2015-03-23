#download LeadFirm.pdf at:
# http://www.dshs.state.tx.us/WorkArea/linkit.aspx?LinkIdentifier=id&ItemID=8589968560
import requests, re, codecs, time
from bs4 import BeautifulSoup
from subprocess import call

call(["pdftotext","-layout","LeadFirm.pdf"], shell=True)

f = open("led_c_TXdhs_%s_000.csv"%time.strftime("%Y%m%d"),"w")

headers = ['file_number','license_number','entity_name','address1','city','state','zip','county','phone','expiration_date','status','issue_date','rank_date']

f.write("|".join(headers)+"\n")
for line in open("LeadFirm.txt","r"):
	if "Phone" not in line:
		nline = re.sub("   *","_%_", line)
		nline = re.sub("\n", "", nline)
		nline = nline.split("_%_")
		if len(nline) > 10:
			f.write("|".join(nline) + "\n")
f.close()

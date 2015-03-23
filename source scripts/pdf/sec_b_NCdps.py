import requests, re, codecs, time
from bs4 import BeautifulSoup
from subprocess import call

#call(["pdftotext","-layout -table","LeadFirm.pdf"])

f = open("sec_b_NCdps_%s_000.csv"%time.strftime("%Y%m%d"),"w")

headers = ['license_number','expiration_date','qualified_individual','entity_name','address1','city state','zip','phone']


f.write("|".join(headers)+"\n")
mark = 3
start = False
for line in open("BurglarAlarmLicensees.txt","r"):
	if 'Number' not in line:
		nline = re.sub("   *","_%_", line)
		nline = re.sub("\n", "", nline)
		nline = nline.split("_%_")
		if len(nline) > 3:
			mark = 0
			start = True
			f.write("|".join(nline))
		elif len(nline) > 1 and mark < 2 and start:
			f.write('|'.join(nline))
			mark += 1
		elif len(nline) > 1 and mark == 2 and start:
			f.write('|'.join(nline) + '\n')
			mark += 1
			start = False
f.close()
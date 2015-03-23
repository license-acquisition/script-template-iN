# Kyle
# Uses URLs pulled by PestURLs.py
from bs4 import BeautifulSoup
import requests, re, time

tally = 0
f = open("pes_c_ALdai_%s_000.csv" %(time.strftime('%Y%m%d')), "w")
headers = ['qualifying_individual', 'company_name', 'county', 'address1', 'city', 'state', 'zip', 'license_number', 'expiration_date', 'license_type2', 'licensee_type_cd', 'company_flag']
f.write("|".join(headers) + "\n")
for line in open("ALpestURLs2.txt", "r"):
	info = []
	for td in BeautifulSoup(requests.get("http://agi-app.alabama.gov/%s"%line).content.replace("<br>", "\",\"")).findAll("td", {"style":"font-size: x-small;"})[1::2]:
		info.append(td.text)
	info[3] = re.sub("(?<!\"),", "", "\",\"".join(info[3].rsplit(" ", 2)))
	info.append('1')
	f.write("|".join(info) + "\n")
        tally+=1
        print tally

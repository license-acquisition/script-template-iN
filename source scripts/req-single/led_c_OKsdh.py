#**********************
# Web Scrape
# Stewart Spencer
# http://www.deq.state.ok.us/aqdnew/lbp/Certified%20Lists/CertifiedLBPFirms.html
# 10/15/2014
#**********************

import csv, re, requests, time, string, codecs
from bs4 import BeautifulSoup

stamp = time.strftime("%Y%m%d")
name = 'led_c_OKsdh_'+stamp+'_000.csv'
f = codecs.open(name,'w','UTF-8')

headers = ["entity_name","license_number","address1","city","state","zip",
           "phone","fax","license_type_cd","number_type","company_flag"]

f.write("|".join(headers) + "\n")

url = 'http://www.deq.state.ok.us/aqdnew/lbp/Certified%20Lists/CertifiedLBPFirms.html'
page = requests.get(url)
soup = BeautifulSoup(page.content)

for tr in soup.find_all('tr'):
    info = []
    for td in tr.find_all('td'):
        info.append(td.text)
    info.append('Certified LBP Firms')
    info.append('Certification Number')
    info.append('1')
    if len(info) > 3:
        f.write("|".join(info) + "\n")
        print("\"" + "\",\"".join(info) + "\"\n")

f.close()
    

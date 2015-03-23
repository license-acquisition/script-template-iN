#**********************************
# Web Scrape
# http://www.portal.state.pa.us/portal/server.pt?open=514&objID=553489&mode=2#f
#
# Stewart Spencer
# 10/02/2014
#**********************************

import csv, re, requests, time, string, codecs
from bs4 import BeautifulSoup

stamp = time.strftime("%Y%m%d")

f = codecs.open('asb_c_PAdli_'+stamp+'_000.csv', 'w', 'UTF-8')

headers = ["license_number","entity_name","phone","address1","city","state","zip","expiration_date","number_type","company_flag"]

f.write("\"" + "\",\"".join(headers) + "\"\n")

#url = 'http://www.portal.state.pa.us/portal/server.pt?open=514&objID=553489&mode=2#f'
#url automatically sends file to downloads, the specific address will vary based who runs the script

html = open('ASBCERT.htm')

soup = BeautifulSoup(html)

info = []

for line in soup.text.split("\n")[4:-3]:
    lic_num = line[0:7]
    name = line[8:32]
    phone = line[33:45]
    address = line[46:110]
    city = line[111:127]
    state = line[128:131]
    zip_code = line[131:142]
    exp_date = line[142:153]

    info.append(lic_num)
    info.append(name)
    info.append(phone)
    info.append(address)
    info.append(city)
    info.append(state)
    info.append(zip_code)
    info.append(exp_date)
    info.append('Certification Number')
    info.append('1')

    f.write("\"" + "\",\"".join(info) + "\"\n")
    print("\"" + "\",\"".join(info) + "\"\n")

    info = []
    
f.close()

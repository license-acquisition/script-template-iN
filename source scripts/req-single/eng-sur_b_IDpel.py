#**********************************
# Web Scrape
# http://www.ipels.idaho.gov/rosterallrecords_1.cfm
#
# Stewart Spencer
# 10/06/2014
#**********************************

import csv, re, time, requests, codecs
from bs4 import BeautifulSoup

url = 'http://www.ipels.idaho.gov/rosterallrecords_1.cfm'

stamp = time.strftime("%Y%m%d")

name = 'eng-sur_b_IDpel_' + stamp + '_000.csv'

f = codecs.open(name, 'w', 'UTF-8')
headers = ["company_flag", "First Name", "entity_name", "Attn", "Address",
           "address1", "city", "state", "zip", "country", "license_number",
           "license authority", "license_type_cd", "status", "retired",
           "first_issue_date", "expiration_date"]

f.write("\"" + "\",\"".join(headers) + "\"\n")

page = requests.get(url)
soup = BeautifulSoup(page.content)
info = []

#Note: This page takes a very long time to load, can be 10+ minutes

for tr in soup.find_all('tr'):
    info.append('1')
    for td in tr.find_all('td'):
        info.append(td.text.replace(u'\xa0',u'').strip())
    f.write("\"" + "\",\"".join(info) + "\"\n")
    print("\"" + "\",\"".join(info) + "\"\n")
    info = []
f.close()

# led_c_MIdch

import codecs, time, requests, re
from bs4 import BeautifulSoup as soupify

f = codecs.open('led_c_MIdch_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['license_number', 'company_name', 'city', 'phone', 'qualifying_individual', 'number_type']
f.write('|'.join(headers) + '\n')

url = 'http://www.michigan.gov/documents/Contractors-all_35972_7.htm'
soup = soupify(requests.get(url).content.replace('&nbsp;', ' '), 'html.parser')

ps = soup.find_all('p', {'class': 'MsoNormal'})

info = []
for p in ps[9:]:
    if len(p.text) > 1 and 'Area Code' not in p.text:
        info.append(p.text.replace('\n','').replace('\r',''))
        if len(info) == 5:
            info.append('certification_number')
            f.write('|'.join(info) + '\n')
            print info
            info = []

f.write('It finished.')
f.close()

import requests, re, codecs, time
from bs4 import BeautifulSoup as soupify
from selenium import webdriver

# create file
f = codecs.open('ele_c_CAbear_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['entity_name', 'licensee_type_cd', 'license_number', 'Registry', 'status', 'address1', 'city', 'zip', 'County',
           'entity_name', 'license_type', 'license_number', 'Registry', 'expiration_date', 'issue_date',
           'city', 'state', 'zip', 'County', 'Action'] 
f.write('|'.join(headers) + '\n')

# set up some stuffz
check = True
start = 1
tally, count = 0, 0
short_url = 'http://www2.dca.ca.gov/pls/wllpub/'
url = 'http://www2.dca.ca.gov/pls/wllpub/WLLQRYNA$LCEV2.QueryList'
payload = {'P_QTE_CODE': 'LIC',
       'P_QTE_PGM_CODE': '5710',
       'P_NAME': '',
       'P_CITY': '',
       'P_COUNTY': '',
       'P_RECORD_SET_SIZE': '500',
       'Z_START': '1',
       'Z_ACTION': 'Find'}

# loop through 500s until dead
fails = 0
while check:
    
    payload['Z_START'] = str(start)
    try:
        # get soup
        print 'Sending request...'
        soup = soupify(requests.get(url, params=payload).content)
        # scrape all the info from data table
        for tr in soup.find_all('table')[0].find_all('tr')[1:]:
            print ' - - - - - %s of %s - - - - -' %(count, tally)
            info1 = []
            for td in tr.find_all('td'):
                info1.append(td.text.strip())
                # find href and get all data from that specific company
                try:
                    if td.find('a')['href'] != '#':
                        soup = soupify(requests.get(short_url + td.find('a')['href']).content)
                        info2 = []
                        for tr in soup.find_all('tr', {'valign': 'TOP'}):
                            info2.append(tr.find_all('td')[1].text.strip())
                except: pass
            # write to file
            f.write('|'.join(info1) + '|' + '|'.join(info2) + '\n')
            print info1 + info2
            count += 1
            tally += 1
    except:
        tally += 1
        fails += 1
    start += 500
    if fails > 10:
        check = False

f.close()

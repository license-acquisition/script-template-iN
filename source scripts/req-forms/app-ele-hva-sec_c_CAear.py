import requests, re, codecs, time
from bs4 import BeautifulSoup as soupify
from selenium import webdriver

# create file
f = codecs.open('rep_c_CAbear_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['entity_name', 'licensee_type_cd', 'license_number', 'status', 'BLANK', 'city', 'zip', 'County',
           'entity_name', 'license_type', 'license_number', 'status', 'expiration_date', 'issue_date',
           'city', 'state', 'zip', 'County', 'Action'] 
f.write('|'.join(headers) + '\n')

# get all the counties
home = 'http://www2.dca.ca.gov/pls/wllpub/wllqryna$lcev2.startup?p_qte_code=SRD&p_qte_pgm_code=3900'
soup = soupify(requests.get(home).content)
options = str(soup.find_all('option')[0]).replace('</option>','')
counties = re.sub('<.*?>', '|', options).split('|')
counties = counties[2:]

# loop through counties till dead
tally, count = 0, 0
short_url = 'http://www2.dca.ca.gov/pls/wllpub/'
url = 'http://www2.dca.ca.gov/pls/wllpub/WLLQRYNA$LCEV2.QueryList'
for county in counties:
    # set up some stuffz
    check = True
    start = 1
    payload = {'P_QTE_CODE': 'SRD',
           'P_QTE_PGM_CODE': '3900',
           'P_NAME': '',
           'P_CITY': '',
           'P_COUNTY': county,
           'P_RECORD_SET_SIZE': '500',
           'Z_START': '1',
           'Z_ACTION': 'Find'}
    print ' - - - - - %s - - - - - ' %(county)
    # loop through 500s until dead
    fails = 0
    while check:
        # add in thing if len of tr is 1, then go to next county
        payload['Z_START'] = str(start)
        try:
            # get soup
            print 'Sending request...'
            soup = soupify(requests.get(url, params=payload).content)
            # check to see if county is done
            if len(soup.find_all('table')[0].find_all('tr')) == 1:
                check = False
            else:
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
f.write('It actually did finish.')
f.close()

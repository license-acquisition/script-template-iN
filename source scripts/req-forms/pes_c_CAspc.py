import requests, re, codecs, time
from bs4 import BeautifulSoup as soupify

start = time.time()

# create file
f = codecs.open('pes_c_CAspc_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['entity_name', 'licensee_type_cd', 'license_number', 'status', 'address1', 'city', 'zip', 'county',
           'entity_name', 'license_type', 'license_number', 'status', 'issue_date', 'LicenseClass',
           'address1', 'city', 'state', 'zip', 'County', 'Action'] 
f.write('|'.join(headers) + '\n')

# get all the counties
home = 'http://www2.dca.ca.gov/pls/wllpub/wllqryna$lcev2.startup?p_qte_code=BUS&p_qte_pgm_code=8400'
soup = soupify(requests.get(home).content)
options = str(soup.find_all('option')[0]).replace('</option>','')
counties = re.sub('<.*?>', '|', options).split('|')
counties = counties[2:-2]
print counties

# loop through counties till dead
logs = []
tally, count = 0, 0
short_url = 'http://www2.dca.ca.gov/pls/wllpub/'
url = 'http://www2.dca.ca.gov/pls/wllpub/WLLQRYNA$LCEV2.ActionQuery'
for county in counties:
    # set up some stuffz
    payload = {
        'P_QTE_CODE': 'BUS',
        'P_QTE_PGM_CODE': '8400',
	'P_BUSINESS_NAME':'',
	'P_LICENSE_NUM': '',
	'P_CITY': '',
	'P_COUNTY': county,
	'P_RECORD_SET_SIZE': '500',
	'Z_ACTION': 'Find'
	}
    check = True
    print ' + + + + + %s + + + + + ' %(county)
    # loop through 500s until dead
    fails = 0
    while check:
        try:
            # get soup
            print 'Sending request...'
            soup = soupify(requests.get(url, params=payload).content)
            print ' - - - - - %s - - - - - ' %(re.search(r'Records [0-9]+ to [0-9]+', soup.text).group())
            logs.append(re.search(r'Records [0-9]+ to [0-9]+', soup.text).group())
            # scrape all the info from data table
            for tr in soup.find_all('table')[0].find_all('tr')[1:]:
                print ' - - - - - %s of %s - - - - -' %(count, tally)
                info1 = []
                for td in tr.find_all('td'):
                    info1.append(td.text.replace('\n','').replace('\r','').strip())
                    # find href and get all data from that specific company
                    try:
                        if td.find('a')['href'] != '#':
                            soup = soupify(requests.get(short_url + td.find('a')['href']).content)
                            info2 = []
                            for tr in soup.find_all('tr', {'valign': 'TOP'}):
                                info2.append(tr.find_all('td')[1].text.replace('\r','').replace('\n','').strip())
                    except: pass
                # write to file
                f.write('|'.join(info1) + '|' + '|'.join(info2) + '\n')
                print info1 + info2
                count += 1
                tally += 1
            # go to next page
            if payload['Z_ACTION'] == 'Next':
                check = False
            else:
                payload['Z_ACTION'] = 'Next'
        except:
            fails += 1
        if fails > 10:
            check = False

final = (time.time() - start)/60.0
f.write('Minutes elapsed: %s \n' %str(final))
f.write('It actually did finish.')
f.close()

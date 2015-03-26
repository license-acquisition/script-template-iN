import requests, re, codecs, time
from bs4 import BeautifulSoup as soupify
from script_template import create_file, logger

# create file and init logger
f = create_file('pes_c_CAspc', 'w', ['12', '32', '21', '37', '0', '4', '44', '8', '12', '32', '21', '37', '19', 'LicenseClass', '0', '4', '36', '44', '8', 'Action'])
l = logger('pes_c_CAspc')

def main():
    # get all the counties
    home = 'http://www2.dca.ca.gov/pls/wllpub/wllqryna$lcev2.startup?p_qte_code=BUS&p_qte_pgm_code=8400'
    soup = soupify(requests.get(home).content)
    counties = []
    for option in soup.find_all('option')[1:-10]:
        counties.append(option['value'])
    l.debug('got counties')
    l.info(counties)

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
        l.debug(' + + + + + %s + + + + + ' %(county))
        # loop through 500s until dead
        fails = 0
        while check:
            try:
                # get soup
                l.debug('Sending request...')
                soup = soupify(requests.get(url, params=payload).content)
                l.debug(' - - - - - %s - - - - - ' %(re.search(r'Records [0-9]+ to [0-9]+', soup.text).group()))
                logs.append(re.search(r'Records [0-9]+ to [0-9]+', soup.text).group())
                # scrape all the info from data table
                for tr in soup.find_all('table')[0].find_all('tr')[1:]:
                    l.debug(' - - - - - %s of %s - - - - -' %(count, tally))
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
                    l.info(info1 + info2)
                    count += 1
                    tally += 1
                # go to next page
                if payload['Z_ACTION'] == 'Next':
                    check = False
                else:
                    payload['Z_ACTION'] = 'Next'
            except Exception as e:
                l.error(str(e))
                fails += 1
            if fails > 10:
                check = False

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()

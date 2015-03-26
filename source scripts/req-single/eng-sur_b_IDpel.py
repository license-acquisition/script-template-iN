#**********************************
# Web Scrape
# http://www.ipels.idaho.gov/rosterallrecords_1.cfm
#
# Stewart Spencer
# 10/06/2014
#**********************************

import csv, re, time, requests, codecs
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('eng-sur_b_IDpel', 'w', ['6', '35', '12', 'qualifying_individual2', 'Address', '0', '4', '36', '44', 'country', '21', 'license authority', '32', '37', 'retired', '19', '13'])
l = logger('eng-sur_b_IDpel')

def main():
	url = 'http://www.ipels.idaho.gov/rosterallrecords_1.cfm'
	s = requests.Session()
	page = s.get(url)
	time.sleep(300) #Note: This page takes a very long time to load, can be 10+ minutes
	soup = BeautifulSoup(page.content)
	info = []

	for tr in soup.find_all('tr'):
	    info.append('1')
	    for td in tr.find_all('td'):
	        info.append(td.text.replace(u'\xa0',u'').strip())
	    f.write('|'.join(info) + '\n')
	    l.info(info)
	    info = []

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
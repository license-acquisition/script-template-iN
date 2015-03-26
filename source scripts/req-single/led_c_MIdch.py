# led_c_MIdch

import codecs, time, requests, re
from bs4 import BeautifulSoup as soupify
from script_template import create_file, logger

f = create_file('led_c_MIdch', 'w', ['21', '7', '4', '33', '35', '102'])
l = logger('led_c_MIdch')

def main():
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
	            l.inf(info)
	            info = []

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
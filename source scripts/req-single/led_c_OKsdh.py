#**********************
# Web Scrape
# Stewart Spencer
# http://www.deq.state.ok.us/aqdnew/lbp/Certified%20Lists/CertifiedLBPFirms.html
# 10/15/2014
#**********************

import csv, re, requests, time, string, codecs
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('led_c_OKsdh', 'w', ['12', '21', '0', '4', '36', '44', '33', '66', '32', '102', '6'])
l = logger('led_c_OKsdh')

def main():
    url = 'http://www.deq.state.ok.us/aqdnew/lbp/Certified%20Lists/CertifiedLBPFirms.html'
    soup = BeautifulSoup(requests.get(url).content)

    for tr in soup.find_all('tr'):
        info = []
        for td in tr.find_all('td'):
            info.append(td.text)
        info.append('Certified LBP Firms')
        info.append('Certification Number')
        info.append('1')
        if len(info) > 3:
            f.write("|".join(info) + "\n")
            l.info(info)
    
if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
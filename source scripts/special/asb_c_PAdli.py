#**********************************
# Web Scrape
# http://www.portal.state.pa.us/portal/server.pt?open=514&objID=553489&mode=2#f
#
# Stewart Spencer
# 10/02/2014
#**********************************

import csv, re, requests, time, string, codecs
from bs4 import BeautifulSoup
from urllib import urlretrieve
from script_template import create_file, logger

f = create_file('asb_c_PAdli', 'w', ['21', '12', '33', '0', '4', '36', '44', '13', '102', '6'])
l = logger('asb_c_PAdli')

#url = 'http://www.portal.state.pa.us/portal/server.pt?open=514&objID=553489&mode=2#f'

def main():
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

        for data in [lic_num, name, phone, address, city, state, zip_code, exp_date, 'Certification Number', '1']:
            info.append(data)

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
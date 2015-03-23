# fir_c_COdfp

import requests, re, codecs, time
from subprocess import call

f = codecs.open('fir_c_COdfp_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['company_name', 'qualifying_individual', 'address1', 'city/state/zip', 'year', 'license_number', 'license_type']
f.write('|'.join(headers) + '\n')

call(['pdftotext', '-layout', '-table', 'fir_c_COdfp.pdf'])

g = codecs.open('fir_c_COdfp.txt', 'r')
lines = g.readlines()
g.close()

for line in lines:
    info = []
    if len(line) > 1 and 'CityStateZip' not in line:
        info = line.replace('\n','').split('  ')
        info = [x.strip() for x in info if len(x) != 0]
        f.write('|'.join(info) + '\n')
        print info

f.close()

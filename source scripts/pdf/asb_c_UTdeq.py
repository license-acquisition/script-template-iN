import requests, re, codecs, time
from subprocess import call
from bs4 import BeautifulSoup

start = time.time()
'''
url = 'http://www.airquality.utah.gov/HAPs/docs/updates/currentcert.pdf'

pdfFile = open('asb_c_UTdeq.pdf', 'w')
pdfFile.write(requests.get(url).content)
pdfFile.close()

call(['pdftotext', '-layout', 'asb_c_UTdeq.pdf'])
'''

# create txt file
f = codecs.open('asb_c_UTdeq_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
f.write('|'.join(['license_number', 'company_name', 'address1', 'city/state/zip', 'phone', 'fax', 'expiration_date']) + '\n')      
# get lines
g = open('asb_c_UTdeq.txt', 'r')
lines = g.readlines()
g.close()
    
right = []
left = []
for line in lines:
        columns = line.split('\t')
        left.append(''.join([columns[0], columns[1]]).strip())
        right.append(''.join([columns[2], columns[3]]).strip())

info = []
fails = 0
for column in [left, right]:
        for line in column:
                if 'Company Certification' in line or 'Compnay' in line or 'Firm Certification' in line:
                        info.append(line)
                        info = [x.replace('"','') for x in info if len(x) != 0]
                        try: # separate license and company
                                int(info[0][0])
                                info.insert(0, info[0][0:3])
                                info[1] = info[1][3:].strip()
                        except:
                                print info
                                pass
                        if len(info) == 6:
                                info.insert(5, '')
                        if len(info) == 7:
                                f.write('|'.join(info) + '\n')
                                print info
                                info = []
                        else:
                                print ' - - - - - - - '
                                print info
                                print ' - - - - - - - '
                                info = []   
                else:
                        info.append(line)
                
f.close()

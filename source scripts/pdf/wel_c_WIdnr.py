# shoutout to Anthony Nault for sound coding logic!
import re, codecs, time, requests
from subprocess import call
from urllib import urlretrieve

# Convert PDF to TEXT (using pdftotext, duh)
#url = 'http://dnr.wi.gov/topic/Wells/documents/WellDrillers.pdf'
#urlretrieve(url, 'wel_c_WIdnr.pdf')
#call(["pdftotext", "-layout", "-table", "wel_c_WIdnr.pdf"])

f = codecs.open('wel_c_WIdnr_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')

# Write headers to data
headers = ['license_number', 'company_name', 'phone1', 'phone2', 'address1/qualifying_individual',
           'city', 'state', 'zip', 'email', 'address1/qualifying_individual']
f.write("|".join(headers) + "\n")

# Read the converted text file.
lines = codecs.open('wel_c_WIdnr.txt', 'r').readlines()

# split into a huge array
rows = []
for line in lines:
    if 'WELL DRILLERS' not in line and 'LIC#' not in line and 'Friday, January' not in line:
        if len(line) != 0:
            row = line.replace('\n','').split('  ')
            for part in row:
                rows.append(part.strip())
rows = [x for x in rows if len(x) != 0]

# get index of comps
index = []
for i in range(len(rows)):
    try:
        if rows[i] == re.search(r'[0-9]{4}', rows[i]).group():
            index.append(i)
    except: pass

# parse data string
for i in range(len(index)-1):
    info = rows[index[i]:index[i+1]]
    if len([x for x, char in enumerate(info) if '(' in char]) != 2:
        info.insert(3, '')
    if len([x for x, char in enumerate(info) if '@' in char]) != 1:
        info.insert(5, '')
    f.write('|'.join(info) + '\n') 
print 'Done.'    
f.close()


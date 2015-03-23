# shoutout to Anthony Nault for sound coding logic!
import re, codecs, time, requests
from subprocess import call
from urllib import urlretrieve

# Convert PDF to TEXT (using pdftotext, duh)
#url = 'http://www.dps.state.ia.us/fm/building/alarm/PDFS/AlarmContractorsListing.pdf'
#urlretrieve(url, 'fir-sec_c_IAdps.pdf')
#call(["pdftotext", "-layout", "-table", "fir-sec_c_IAdps.pdf"])

f = codecs.open('fir-sec_c_IAdps_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')

# Write headers to data
headers = ["entity_name", "license_number", "address1", "city", "state", "zip", "phone", "expiration_date",
           "qualifying_individual", "licensee_type_cd", "...", "qualifying_individual2", "licensee_type_cd2"]
f.write("|".join(headers) + "\n")

# Read the converted text file.
lines = codecs.open('fir-sec_c_IAdps.txt', 'r').readlines()

# split into a huge array
rows = []
for line in lines:
    if 'Iowa Department of' not in line and 'State Fire Marsh' not in line and 'Alarm System Lic' not in line and 'Des Moines, IA 50319' not in line and '(515) 725-6145' not in line and 'Business Name' not in line and 'Friday, February' not in line:
        if len(line) != 0:
            row = line.replace('\n','').split('  ')
            for part in row:
                rows.append(part.strip())
rows = [x for x in rows if len(x) != 0 and 'RME:' not in x]

# get index of comps
index = []
for i in range(len(rows)):
    try:
        re.search(r'AC-[0-9]{3}', rows[i]).group()
        index.append(i-1)
    except: pass

# parse data string
info = []
for i in range(len(index)-1):
    f.write('|'.join(rows[index[i]:index[i+1]]) + '\n')

print 'Done.'    
f.close()

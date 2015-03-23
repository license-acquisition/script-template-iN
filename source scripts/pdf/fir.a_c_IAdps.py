import requests, re, time, codecs
from subprocess import call
from bs4 import BeautifulSoup

#open("fir.b_c_IAdps.pdf", "w").write(requests.get("http://www.dps.state.ia.us/fm/building/fesccp/PDFs/FESCCP_CertInstallers.pdf").content)
#call(["pdftotext", "-layout", "-table", "fir.b_c_IAdps.pdf"])

f = codecs.open('fir.b_c_IAdps_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['company_name', 'license_number', 'qualifying_individual', 'license_number2', 'JobTitle', 'date', 'licensee_type_cd']
f.write('|'.join(headers) + '\n')

# Read the converted text file.
lines = codecs.open('fir.b_c_IAdps.txt', 'r').readlines()

# split into a huge array
rows = []
for line in lines:
    if not any(s in line for s in ['Iowa Department', 'State Fire Marsha', '215 E Seventh', 'Wednesday, Feb', 'Des Moines, IA 50319','515) 725-6145','Licensed Fire Protection']):
        if len(line) > 1:
            row = line.replace('\n','').split('  ')
            for part in row:
                rows.append(part.strip())
rows = [x.strip() for x in rows if len(x) != 0]

# get index of comps
index = []
for i in range(len(rows)):
    try:
        if rows[i] == re.search(r'FP-[0-9]{3}', rows[i]).group():
            index.append(i)
    except: pass

# parse data string
for i in range(len(index)-1):
    info = rows[index[i]-1:index[i+1]-1]
    f.write('|'.join(info) + '\n')
    print info
info = rows[index[len(index)-1]-1:]
f.write('|'.join(info) + '\n')
print 'Done.'    
f.close()

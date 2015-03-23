import requests, re, codecs, time
from subprocess import call
from bs4 import BeautifulSoup

#open("fir_c_DEsfm.pdf", "w").write(requests.get("http://statefiremarshal.delaware.gov/pdfs/pubfass.pdf").content)
#call(["pdftotext", "-layout", "-table", "fir_c_DEsfm.pdf"])
# ---- Removed all of the class info manually

f = codecs.open('fir_c_DEsfm_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['entity_name', 'address1', 'city/state/zip', 'phone', 'fax', 'licese_number', 'email']
f.write('|'.join(headers) + '\n')

g = codecs.open('fir_c_DEsfm_manual.txt', 'r')
lines = g.readlines()
g.close()

left = []
middle = []
right = []
lines = [x for x in lines if len(x)>1]
for line in lines:
    columns = line.replace('\n','').split('\t')
    left.append(columns[0].strip())
    middle.append(columns[1].strip())
    right.append(columns[2].strip())

count = 0
for column in [left, middle, right]:
    data = [x for x in column if len(x)!=0]
    
    index = []
    for i in range(len(data)):
        if 'License' in data[i]:
            index.append(i)
        if 'www.' in data[i]:
            index.append(i)
    remove = []
    for j in range(len(index)-2):
        if index[j+1] - index[j] == 1:
            remove.append(index[j])

    for n in remove:
        index = [x for x in index if x != n]

    for k in range(len(index)-2):
        if k==0:
            info2 = data[:index[k]]
            info = data[index[k]+1:index[k+1]+1]
            f.write('|'.join(info2) + '\n')
        else:
            info = data[index[k]+1:index[k+1]+1]
        print info
        f.write('|'.join(info) + '\n')

f.close()

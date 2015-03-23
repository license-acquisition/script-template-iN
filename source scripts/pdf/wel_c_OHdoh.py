import requests, re, time, codecs
from subprocess import call
from bs4 import BeautifulSoup

#open("wel_c_OHdoh.pdf", "w").write(requests.get("http://www.sfm.illinois.gov/documents/Licensed_fire_sprinkler_contractors06052014.pdf").content)
#call(["pdftotext", "-layout", "-table", "wel_c_OHdoh.pdf"])

f = codecs.open("wel_c_OHdoh_%s_000.txt" %(time.strftime('%Y%m%d')), "w")
f.write("license_number, entity_name, qualifying_individual, YEAR, address1, phone, city, state, zip, issue_date, status\n".replace(',', '|'))

g = codecs.open('wel_c_OHdoh.txt', 'r')
lines = g.readlines()
g.close()

info = []
for i in range(len(lines)):
        if len(lines[i]) > 1 and not any(s in lines[i] for s in ['Ohio Department','Contractor Activity','Well  Spring','Total Number of','of 85']):
                for data in lines[i].replace('\n', '').split('  '):
                        info.append(data.strip())
info = [x.replace(')','').replace('(','') for x in info if len(x) != 0 and x!='X']

index1 = [x for x, char in enumerate(info) if char=='Active']
index2 = []
for k in range(len(info)):
        try:
                re.search(r'[0-9]{6}', info[k]).group()
                index2.append(k)
        except:
                pass
        
for j in range(len(index1)):
        if j == len(index1)-1:
                info2 = info[index1[j]-8:]
        else:
                info2 = info[index2[j]:index1[j]+1]
        try:
                addrs = info2[6]
                del(info2[6])
                info2.insert(6, addrs.rsplit(' ',2)[0].strip()) # city
                info2.insert(7, addrs.rsplit(' ',2)[1].strip()) # state
                info2.insert(8, addrs.rsplit(' ',2)[2].strip()) # zip
        except:
                pass
        if len(info2) == 11:
                print info2
                f.write('|'.join(info2) + '\n')


f.close()

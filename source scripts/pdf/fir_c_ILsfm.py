import requests, re, time, codecs
from subprocess import call
from bs4 import BeautifulSoup
#open("fir_c_ILsfm.pdf", "w").write(requests.get("http://www.sfm.illinois.gov/documents/Licensed_fire_sprinkler_contractors06052014.pdf").content)
#call(["pdftotext", "-layout", "-table", "fir_c_ILsfm.pdf"])

f = codecs.open("fir_c_ILsfm_%s_000.txt" %(time.strftime('%Y%m%d')), "w")
f.write("company_name, address1, city, state, zip, license_number, start_date, expiration_date, first_issue_date, license_type, status\n".replace(',', '|'))

g = codecs.open('fir_c_ILsfm.txt', 'r')
lines = g.readlines()
g.close()

info = []
for i in range(len(lines)):
        if len(lines[i]) > 1 and not any(s in lines[i] for s in ['License Detail','Search Criteria','JURISDICTION ONLINE','Praeses Corporation','License #']):
                for data in lines[i].replace('\n', '').split('  '):
                        info.append(data.strip())
info = [x for x in info if len(x) != 0]

index1 = [x for x, char in enumerate(info) if char == 'License']
for i in index1: # joining spacing between 'Fire Sprinkler Contractor' and 'License'
        info[i-1] = ' '.join([info[i-1], info[i]])
info = [x for x in info if x != 'License']

index = [x for x, char in enumerate(info) if 'Active' in char or 'Lapsed' in char]
              
for j in range(len(index)):
        if j == len(index)-1:
                info2 = info[index[j]-6:]
        else:
                info2 = info[index[j]-6:index[j+1]-6]
        if len(info2) == 8:
                info2[0] = ' '.join([info2[0],info2[1]])
                del(info2[1])
        addrs = info2[0]
        del(info2[0])
        info2.insert(0, addrs.rsplit(',', 2)[0].rsplit('-',1)[0].strip()) # company_name
        info2.insert(1, addrs.rsplit(',', 2)[0].rsplit('-',1)[1].strip()) # address1
        info2.insert(2, addrs.rsplit(',', 2)[1].strip()) # city
        info2.insert(3, addrs.rsplit(',',2)[2].strip()[:2]) # state
        info2.insert(4, addrs.rsplit(',',2)[2].strip()[2:].strip()) # zip
        print info2
        f.write('|'.join(info2) + '\n')


'''   

last = []
for line in open("fir_c_ILsfm.txt", "r"):
	if not any(s in line for s in ['License Detail Report','Search Criteria','JURISDICTION ONLINE','Praeses Corporation','License #']):
		nline = re.sub("   *", "_%_", line)
		nline = re.sub("\n", "", nline)
		nline = nline.split("_%_")
		if len(line)>5:
			if nline[0] == "":
				
				for item in nline[1:]:
					last.append(item)
				last[0] = "|".join(last[0].rsplit(' ',2))
				last = "|".join(last).split("|")
				last[0] = last[0].strip(",")
				last[0] = "|".join(last[0].rsplit('|',1))
				last[0] = "|".join(last[0].rsplit('-',1))
				f.write("|".join(last) + "\n")
				last = []
			else:
				for item in nline:
					last.append(item)	
f.close()
'''

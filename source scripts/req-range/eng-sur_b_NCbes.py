import sys
import re
import requests
import codecs, time
from bs4 import BeautifulSoup

# North Carolina Engineers

# Name, Business Name, Address, City, State, Zip, License Number, Status, expiration date

# From: https://www.membersbase.com/ncbels-vs/public/searchdb.asp
start = time.time()
f = codecs.open('eng-sur_b_NCbes_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['entity_name', 'Business Name', 'address1', 'city/state/zip', 'phone', 'license_number', 'status', 'licensee_type_cd']
f.write('|'.join(headers) + '\n')

multi_lic = {}
for license_type in ['P']: # original ['C', 'D', 'F', 'P']
        for i in range (1384, 10000): # original (1000, 10000)
                print ' - - - - - Searching license %s-%s - - - - - ' %(license_type, i)
                url = "https://www.membersbase.com/ncbels-vs/public/dosearchdb.asp?%s-%04d" %(license_type, i)      
                page = requests.get(url)
                newcon = re.sub('<br>', '_', page.content)
                newcon = re.sub('&nbsp;', ' ', newcon)
                soup = BeautifulSoup(newcon)
                div = soup.find(["b"])
                if 'Click on the license number for details' in soup.text:
                        multi_lic[license_type] = i
                        pass
                elif div.text == "Search Registrant Directory":
                        print "Invalid License Number"
                else:
                        info = []
                        dat = div.parent
                        nameAddress = dat.text.split('_')
                        if len(nameAddress) == 4:
                                info.append(nameAddress[0].strip()) #entity_name
                                info.append(' ')
                                info.append(nameAddress[1].strip()) # address1
                                info.append(nameAddress[2].strip()) # state
                                info.append(nameAddress[3].strip()) # phone
                        else: # length of 5
                                info.append(nameAddress[0].strip()) # entity_name
                                info.append(nameAddress[1].strip()) # BusinessName
                                info.append(nameAddress[2].strip()) # address1
                                info.append(nameAddress[3].strip()) # state
                                info.append(nameAddress[4].strip()) # phone
                        dat2 = dat.nextSibling
                        license_num = re.sub(".*License:", '', dat2.text).strip()
                        info.append(re.sub('_.*', '', license_num)) # license_num
                        status = re.sub(".*Status:", '', dat2.text).strip()
                        info.append(re.sub('_.*', '', status)) # status
                        expires =re.sub(".*Service:", '', dat2.text).strip()
                        info.append(re.sub('_.*', '', expires)) # expiration_date
                        print info
                        f.write('|'.join(info) +'\n')

f.write('It actually finished. \n')
f.write('Minutes Elapsed: %s \n' %((time.time()-start)/60.0))
f.close()

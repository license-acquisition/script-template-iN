import sys
import re
import requests
import codecs, time
from bs4 import BeautifulSoup
from script_template import create_file, logger

# North Carolina Engineers

# From: https://www.membersbase.com/ncbels-vs/public/searchdb.asp
f = create_file('eng-sur_b_NCbes', 'w', ['12', 'Business Name', '0', 'city/state/zip', '33', '21', '37', '32'])
l = logger('eng-sur_b_NCbes')

def main():
        multi_lic = {}
        for license_type in ['C', 'D', 'F', 'P']: # original ['C', 'D', 'F', 'P']
                for i in range (1000, 10000): # original (1000, 10000)
                        l.debug(' - - - - - Searching license %s-%s - - - - - ' %(license_type, i))
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
                                l.debug("Invalid License Number")
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
                                l.info(info)
                                f.write('|'.join(info) +'\n')

if __name__ == '__main__':
        try:
                main()        
                l.info('complete')
        except Exception as e: l.critical(str(e))
        finally: f.close()
import sys, codecs, time, requests
from bs4 import BeautifulSoup

count = 1160031

#f=open("AL_homebuildtest4.csv","a") # append to original file
f = codecs.open('bui_b_ALhlb_%s_000.csv' %(time.strftime('%Y%m%d')), 'w', 'utf-8') # new file
headers = ['entity_name', 'license_number', 'licensee_type_cd', 'expiration_date', 'county', 'address1', 'zip','status']
f.write('|'.join(headers)+'\n')
#1197916
for i in range(1182744,1200000):
    info = []
    try:
        url = "https://alhob.glsuite.us/GLSuiteweb/clients/alhob/public/LicenseeDetails.aspx?EntityID=%d" %(i)
        soup = BeautifulSoup(requests.get(url).content)
        info.append(soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblBusinessName"}).text.strip()) # licname
        info.append(soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblLicNum"}).text.strip()) # licnumb
        info.append(soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblLicType"}).text.strip()) #lictype
        info.append(soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblLicExpire"}).text.strip()) # licexp
        info.append(soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblCounty"}).text.strip()) # liccount
        info.append(soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblStreet"}).text.strip()) # licaddr
        info.append(soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblCityStateZip"}).text.strip()) # licstzip
        info.append(soup.find("span", {"id" : "ctl00_ContentPlaceHolder1_lblLicStatus"}).text.strip()) # licstat

        print info[0:3]
        f.write('|'.join(info) + '\n')
    except:
        print('Alabama Home Builders...')
        #print url
        count += 1
        print count
    	
f.close()

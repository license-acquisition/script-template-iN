import sys, codecs, time, requests
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('bui_b_ALhlb', 'w', ['12', '21', '32', '13', '8', '0', '44', '37'])
l = logger('bui_b_ALhlb')

def main():
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

            l.info(info[0:3])
            f.write('|'.join(info) + '\n')
        except Exception as e:
            l.error('Error on %s: %s' %i, str(e))
    	
if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
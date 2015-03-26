# -*- coding: utf-8 -*-
import requests,re
from bs4 import BeautifulSoup
import codecs
from string import ascii_letters, digits
from datetime import date
import time
from script_template import create_file, logger

f = create_file('ele-c_NY.NYdob', 'w', ['12', 'firm_number', '19', 'general_liability', '37', "Worker's Compensation", '33', '32', '6', 'url', '0', '36', '44'])
l = logger('ele-c_NY.NYdob')

def main():
    s = requests.Session()
    #check range
    for i in range(1,6000):
        time.sleep(1)
        l.info(i)
        try:
            # set up cache before searching
            s.get('http://a810-bisweb.nyc.gov/bisweb/LicenseTypeServlet?vlfirst=Y')
            url = "http://a810-bisweb.nyc.gov/bisweb/LicenseQueryServlet?licensetype=B&licno=%06d&requestid=2"%i
            soup = BeautifulSoup(s.get(url).content)
            info = []
            test = []
            test2 = []
            data = soup.find_all("td",{"class":"content"})
            data2 = soup.find_all("td",{"class":"content","colspan":"3"})
            data3 = soup.find_all("td",{"class":"tblhdg"})
            data4 = soup.find_all("td",{"class":"content","colspan":"5"})

            for app2 in data4:
                test2.append(app2.text)

            for app in data2:
                test.append(app.text)

            first_issue_date = data[0].text
            firmnumber = data[1].text
            status = data[3].text
            #print test
            if len(test2) == 3:
                entity_name = data[6].text
                #print entity_name
                general_liability = data[8].text
                gl_company = data[9].text
                wc = data[11].text
                address1 = data[18].text
                licensetype = data3[0].text
                licensetype = re.sub("====","",licensetype)

                if len(test) == 3:
                    
                    phone = data[20].text
                    name = data[21].text
                    expiration_date = data[24].text
                    license_number = data[22].text
                    strip0 = re.sub("Business 1  :",'',entity_name)
                    strip1 = re.sub("Firm #:",'',firmnumber)
                    strip2 = re.sub("Date Issued:",'',first_issue_date)
                    strip3 = re.sub("Status:",'',status)

                    info.append(u''.join(i for i in strip0 if ord(i)<128))
                    info.append(u''.join(i for i in strip1 if ord(i)<128))
                    
                    info.append(u''.join(i for i in strip2 if ord(i)<128))
                    info.append(u''.join(i for i in general_liability if ord(i)<128))
                    info.append(u''.join(i for i in strip3 if ord(i)<128))
                    info.append(wc)
                    info.append(phone)
                    info.append(licensetype)
                    info.append("1")
                    info.append(url)
                    info.append("".join(i for i in address1 if ord(i)<128))
                    info[10] = "\"|\"".join(info[10].rsplit(", ", 1))
                    info[10] = "\"|\"".join(info[10].rsplit(" ", 1))
                    
                    l.info(info)
                    f.write("\"" + "\"|\"".join(info) + "\"\n")

                elif len(test)==4:
                    address = data[18].text + data[19].text
                    phone = data[22].text
                    name = data[23].text
                    expiration_date = data[26].text
                    license_number = data[24].text
                    strip0 = re.sub("Business 1  :",'',entity_name)
                    strip1 = re.sub("Firm #:",'',firmnumber)
                    strip2 = re.sub("Date Issued:",'',first_issue_date)
                    strip3 = re.sub("Status:",'',status)    
                    info.append("".join(i for i in strip0 if ord(i)<128))       
                    info.append("".join(i for i in strip1 if ord(i)<128))
                    
                    info.append("".join(i for i in strip2 if ord(i)<128))
                    info.append("".join(i for i in general_liability if ord(i)<128))
                    info.append("".join(i for i in strip3 if ord(i)<128))
                    info.append(wc)
                    info.append(phone)        
                    info.append(licensetype)
                    info.append("1")
                    info.append(url)
                    info.append("".join(i for i in address if ord(i)<128))
                    info[10] = "\",\"".join(info[10].rsplit(", ", 1))
                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                    l.info(info)
                    f.write("\"" + "\"|\"".join(info) + "\"\n")

            elif len(test2)==4:
                entity_name = data[7].text
                general_liability = data[9].text
                gl_company = data[10].text
                wc = data[12].text
                address1 = data[19].text
                licensetype = data3[0].text
                licensetype = re.sub("====","",licensetype)


                if len(test) == 3:
                    phone = data[21].text
                    name = data[23].text
                    expiration_date = data[24].text
                    license_number = data[22].text
                    strip0 = re.sub("Business 1  :",'',entity_name)
                    strip1 = re.sub("Firm #:",'',firmnumber)
                    strip2 = re.sub("Date Issued:",'',first_issue_date)
                    strip3 = re.sub("Status:",'',status)
                    info.append("".join(i for i in strip0 if ord(i)<128))        
                    info.append("".join(i for i in strip1 if ord(i)<128))
                    
                    info.append("".join(i for i in strip2 if ord(i)<128))
                    info.append("".join(i for i in general_liability if ord(i)<128))
                    info.append("".join(i for i in strip3 if ord(i)<128))
                    info.append(wc)
                    info.append(phone)   
                    info.append(licensetype)
                    info.append("1")
                    info.append(url)
                    info.append("".join(i for i in address1 if ord(i)<128))
                    info[10] = "\",\"".join(info[10].rsplit(", ", 1))
                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                    
                    l.info(info)
                    f.write("\"" + "\"|\"".join(info) + "\"\n")

                elif len(test)==4:
                    address = data[18].text + data[19].text
                    phone = data[22].text
                    name = data[23].text
                    expiration_date = data[26].text
                    license_number = data[24].text
                    strip0 = re.sub("Business 1  :",'',entity_name)
                    strip1 = re.sub("Firm #:",'',firmnumber)
                    strip2 = re.sub("Date Issued:",'',first_issue_date)
                    strip3 = re.sub("Status:",'',status)         
                    info.append("".join(i for i in strip0 if ord(i)<128))       
                    info.append("".join(i for i in strip1 if ord(i)<128))
                    
                    info.append("".join(i for i in strip2 if ord(i)<128))
                    info.append("".join(i for i in general_liability if ord(i)<128))
                    info.append("".join(i for i in strip3 if ord(i)<128))
                    info.append(wc)
                    info.append(phone)         
                    info.append(licensetype)
                    info.append("1")
                    info.append(url)
                    info.append("".join(i for i in address if ord(i)<128))
                    info[10] = "\",\"".join(info[10].rsplit(", ", 1))
                    info[10] = "\",\"".join(info[10].rsplit(" ", 1))
                    l.info(info)
                    f.write("\"" + "\"|\"".join(info) + "\"\n")

        except Exception, e:
            l.error(str(e))

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()

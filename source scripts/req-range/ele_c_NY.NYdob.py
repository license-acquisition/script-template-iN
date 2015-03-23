# -*- coding: utf-8 -*-
import requests,re
from bs4 import BeautifulSoup
import codecs
from string import ascii_letters, digits
from datetime import date
import time

start = time.time()
s = requests.Session()
l = codecs.open("ele_c_NY.NYdob_%s_000.txt" %(time.strftime('%Y%m%d')), 'w', 'utf-8')
l.write("entity_name|firm_number|first_issue_date|general_liability|status|Worker's Compensation|phone|licensee_type_cd|company_flag|url|address1|state|zip\n")



#check range
for i in range(1,6000):
    time.sleep(1)
    print i
    try:
        url = "http://a810-bisweb.nyc.gov/bisweb/LicenseQueryServlet?licensetype=B&licno=%06d&requestid=2"%i
        #print url
        source = s.get(url)
        soup = BeautifulSoup(source.content)
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
                
                print info
                l.write("\"" + "\"|\"".join(info) + "\"\n")

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
                print info
                l.write("\"" + "\"|\"".join(info) + "\"\n")

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
                
                print info
                l.write("\"" + "\"|\"".join(info) + "\"\n")

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
                print info
                l.write("\"" + "\"|\"".join(info) + "\"\n")

    except Exception, e:
        print str(e)


l.close()

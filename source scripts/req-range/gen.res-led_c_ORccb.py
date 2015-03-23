import sys, requests, codecs, time, re, csv, string
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
start=time.time()
year=date.today().year
month=date.today().month
day=date.today().day

f = codecs.open("gen.res_c_ORccb_%s_000.csv"%(time.strftime("%Y%m%d")),"a","utf-8")
f.write("license_number,status,first_issue_date,entity_name,company_flag,address1,city,zip,phone,licensee_type_cd,primary_specialty,secondary_specialty\n")
s = requests.session()
s.get("http://search.ccb.state.or.us/search/")

for i in range (1,250000):

    url = "http://www.ccb.state.or.us/search/search_results.asp?regno=%6d" %i
    page = s.get(url)
    soup = BeautifulSoup(page.content)
    url2 = "http://www.ccb.state.or.us/search/business_detail.asp?license_number=%6d" %i

    try:

        info2 = []
        info = []

        data = soup.findAll('tr',{"class":"bodyText"})

        for tex in data:
            

            for texto in tex.findAll('td'):

                info2.append((texto.text).strip())
                
        info.append(info2[2])
        info.append(info2[5])
        info.append(info2[7])
        info.append(info2[9])
        info.append("1")
        

        if len(info)>2:

            page2 = s.get(url2)
            soup = BeautifulSoup(page2.content)

            data2 = soup.findAll('td',{"colspan":"3"})

            info.append((data2[2].text).strip())
            info.append((data2[3].text).strip())
            info.append((data2[4].text).strip())

            info[5] = "\",\"".join(info[5].rsplit(" ",1))
            info[5] = "\",\"".join(info[5].rsplit(" ",1))

            info[7] = (re.sub('\r\n','',info[7]))

            try: 
                info[7] = "\",\"".join(info[7].split(":",1))
                info[7] = "\",\"".join(info[7].rsplit("Commercial:",1))
       
                

            except:
                continue

            info[7] = info[7].strip()

            print info

            print "\"" + "\",\"".join(info) + "\"\n"
            f.write ("\"" + "\",\"".join(info) + "\"\n")

        else:
            continue
        
         

    except Exception, e:

        print str(e)
         
                
f.close()
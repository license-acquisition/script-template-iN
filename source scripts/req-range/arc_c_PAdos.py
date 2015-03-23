import sys, requests, codecs, time, re, csv, string
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits
start=time.time()
year = date.today().year
month = date.today().month
day = date.today().day

f = codecs.open('arc_c_PA_%s%s%s_000k.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')
#g = open("arc_c_PA_links.txt", "w")
f.write("entity_name|city|state|zip|licensee_type_cd|license_number| |professions|status|first_issue_date|expiration_date|last_renew_date|company_flag\n")

s = requests.session()
s.get("http://www.licensepa.state.pa.us/Search.aspx?facility=Y")


try:

    for i in range (30000,35000):
        url = "http://www.licensepa.state.pa.us/Details.aspx?agency_id=1&license_id=%d&"%i
        page=s.get(url)
        time.sleep(1)
        soup = BeautifulSoup(page.content)
        
        try:
            
            info = []
            info.append((soup.find("span", id="_ctl17__ctl1_full_name")).text)
            info.append((soup.find("span", id="_ctl22__ctl1_addr_line_4")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_license_type")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_license_no")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_sec_license_type")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_profession_id")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_sec_lic_status")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_Issue_Date")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_Expiration_Date")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_date_last_renewal")).text)
            info.append("1")

            info[1] = "\",\"".join(info[1].rsplit(" ", 1))
            info[1] = "\",\"".join(info[1].rsplit(" ", 1))
            

        except Exception, e:
            print str(e)
            continue
        print i    
        print "\"" + "\",\"".join(info) + "\"\n"
        f.write("|".join(info) + "\n")

except Exception, e:
    print str(e)
       




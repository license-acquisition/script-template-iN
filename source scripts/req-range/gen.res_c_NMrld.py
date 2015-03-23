import time, sys, requests, re, codecs, csv
from bs4 import BeautifulSoup
from datetime import date
start=time.time()
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open('gen.res_c_NMpsi_%s_000.csv' % (str(year) + str(month).zfill(2) + str(day).zfill(2)), 'w', 'utf-8')
f.write("number_type, licensee_type_cd, company_flag, license_number, phone, status, first_issue_date, expiration_date, volume, address1, city, state, zip, qualifying_individual, qpcertificate no1, qpclassification1, qpattach date1, qpstatus1, qualifying_individual, qpcertificate no2, qpclassification2, qpattach date2, qpstatus2\n")
largeGap = 1000
gap = 0
i=0
while True:
    try:
        print i
        i+=1
        gap+=1
        if gap>largeGap*2 and i > 51481:
            break   
        url = "https://public.psiexams.com/licensee/showBusinessLicensee.do?licenseId=%d&licenseApplicationId=173501" %i

        page = requests.get(url)
        soup = BeautifulSoup(page.content)
        tr = soup.find_all("tr")
        td = soup.find_all("td")
        fieldlabel = soup.find_all("fieldlabel")

        data = []

        data.append("License Number")
        data.append("Contractor")
        data.append(soup.find_all("td", {"class" : "fieldlabel"})[0].next)
        data.append(soup.find_all("td", {"class" : "fieldlabel"})[2].next)
        data.append(soup.find_all("td", {"class" : "fieldlabel"})[4].next)
        data.append(soup.find_all("td")[20].next)
        data.append(soup.find_all("td", {"class" : "fieldlabel"})[7].next)
        data.append(soup.find_all("td")[25].next)
        data.append(soup.find_all("td", {"class" : "fieldlabel"})[10].next)
        data.append(soup.find_all("td", {"class" : "fieldlabel"})[12].next)
        data.append(soup.find_all("td")[38].next)
        data.append(soup.find_all("td", {"class" : "fieldlabel"})[14].next)
        data.append(soup.find_all("td", {"class" : "fieldlabel"})[16].next)
        data.append(soup.find_all("td", {"class" : "fieldlabel"})[18].next)

        wr = (soup.find("tr", {"class" : "whiterow"})).find_all("tr")
        del(wr[0])
        for row in wr:
            for td in row.find_all("td"):
                data.append(td.text)    
        del(data[10])
        f.write('\"' + "\",\"".join(data) + "\"\n")
        print('\"' + "\",\"".join(data) + "\"\n")
        if gap>largeGap:
            largeGap = gap
        gap = 0
    except Exception as e:
    
        print str(e)
        
print time.time()-start

f.close()



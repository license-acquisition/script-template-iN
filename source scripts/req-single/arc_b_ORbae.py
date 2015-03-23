import sys, requests, codecs, time, re, csv, string
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits

start=time.time()
year=date.today().year
month=date.today().month
day=date.today().day
#automate date naming of file

f=codecs.open('arc_b_ORbae_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')
f.write("entity_name|license_number|status|disciplinary_status|address1|city|state|zip|first_issue_date|expiration_date|HSW|company_flag|licensee_type_cd\n")
#create a .csv file and write the appropriate headings in the file

url='http://orbae.com/database/search_architects.php?status=Active&fname=&mi=&lname=&firm=&license=&city=&state=&option=com_content&task=view&id=20&Itemid=1'
page=requests.get(url)
soup=BeautifulSoup(page.content.replace("<br>"," "))

#grab the html for the page

list1=[]
td=soup.findAll('td')
i=0
for one in td[1::6]:
    list1.append(one.text)
    
    two=td[2+(6*i)].text
    list1.append(two)
    
    three=td[3+(6*i)].text.replace(",","")
    three="\",\"".join(three.rsplit(" ", 3))
    list1.append(three)
    
    four=td[4+(6*i)].text
    d=four[0:10]
    e=four[10:]
    list1.append(d)
    list1.append(e)
    
    five=td[5+(6*i)].text
    list1.append(five)

    part1 = "|".join(list1[0].rsplit(" ",1))
    list1[1] = "|".join(list1[1].rsplit(" ",1))

    determineCom = list1[0].rsplit("(",1)
    if "AF" in determineCom[1]:
        list1.append("1")
        list1.append("Architecture Firm")
    
    print("\"" + "\",\"".join(list1) + "\"\n")
    f.write("|".join(list1) + "\n")
    list1=[]
    i=i+1
    
f.close()

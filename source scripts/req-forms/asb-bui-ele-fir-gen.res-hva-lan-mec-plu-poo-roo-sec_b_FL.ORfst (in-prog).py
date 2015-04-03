#-*- coding: cp1252 -*-
import requests, re, time, codecs, sys

from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits
import time
from script_template import create_file, logger

f = create_file('asb-bui-ele-fir-gen.res-hva-lan-mec-plu-poo-roo-sec_b_FL.ORfst', 'w', ['21', '37', 'Application Date', '32', '78', '19', '13', 'description', 'applicant', 'name', '0', '36', '44', 'nothing', '33', '6', '7', '12', '102'])
l = logger('asb-bui-ele-fir-gen.res-hva-lan-mec-plu-poo-roo-sec_b_FL.ORfst')
s = requests.Session()

def main():
    shortie = 'https://fasttrack.ocfl.net/PublicPortal/OC/SearchContractor.jsp'
    soup = BeautifulSoup(s.get(shortie).content)
    peach = []
    for sbe in soup.find_all('option')[1:]:
        peach.append(sbe['value'])
    l.debug(peach)
    for core in peach:
        try:
            l.debug('Searching License Type: %s - - - - - -' %core)
            url = shortie+'?lid=ReadOnlyoc&breadcrumbName=My+Services&breadcrumbValue=&secondLevelBreadcrumbName=No&secondLevelBreadcrumbValue=No&thirdLevelBreadcrumbName=No&thirdLevelBreadcrumbValue=No&SubCode=%s&ReferenceFile=&ZipCode=&NameFirst=&NameLast=&OrganizationName=&query=Yes&FolderRSN=&OrderBy=FolderRSN&OrderByAsc=DESC&sortingCheck=true' %core
            soup = BeautifulSoup(s.get(url).content)
            length = soup.find_all("tr",{"class":"FormtableData1"})
            length2 = soup.find_all("tr",{"class":"FormtableData2"})
            apple = []
            for a in length:
                apple.append(a.text)
            for b in length2:
                apple.append(b.text)

            for link in soup.find_all('a', {'class': 'alink'}):
                try:
                    form_data = []
                    onclick = link['onclick'].replace('f_details(\'','').replace('\');','')
                    form_data.append(onclick.split(',')[0].replace('\'',''))
                    form_data.append(onclick.split(',')[1].replace('\'',''))
                    l.debug('Searching %s %s - - - - - - - - - -' %(form_data[0], form_data[1]))
                    shorty = 'https://fasttrack.ocfl.net/PublicPortal/OC/SearchContractor_Detail.jsp'
                    url = shorty + '?lid=ReadOnlyoc&breadcrumbName=Licensed+Contractors&breadcrumbValue=SearchContractor.jsp&secondLevelBreadcrumbName=Inspections&secondLevelBreadcrumbValue=Inspections&thirdLevelBreadcrumbName=%s&thirdLevelBreadcrumbValue=No&SubCode=%s&ReferenceFile=&ZipCode=&NameFirst=&NameLast=&OrganizationName=&query=&FolderRSN=%s&OrderBy=FolderRSN&OrderByAsc=ASC&sortingCheck=true' %(form_data[1], core, form_data[0])
                    soup = BeautifulSoup(s.get(url).content)
                    info = []                      
                    for tr in soup.find_all('tr',{"class":"FormtableData1"}):
                        for dat in tr.find_all("td"):
                            info.append(dat.text)
                    try:
                        if len(info[10])>3:                
                            info[10] = info[10].strip()
                            info[10] = "|".join(info[10].rsplit(" ", 1))
                            info[10] = "|".join(info[10].rsplit(" ", 1))
                            info[10] = re.sub("Phone:","",info[10])
                            info[10] = "|".join(info[10].rsplit(" ", 1))
                            info[10] = "|".join(info[10].rsplit(" ", 1))
                        else:
                            info[10] = "     "
                            info[10] = "|".join(info[10].rsplit(" ", 1))
                            info[10] = "|".join(info[10].rsplit(" ", 1))
                            info[10] = "|".join(info[10].rsplit(" ", 1))
                            info[10] = "|".join(info[10].rsplit(" ", 1))              
                    except:
                        pass
                    try:
                        if len(info[11])>1:
                    
                            info[11] = re.sub(u"Â","",info[11])
                            info[11] = re.sub("Escrow",'',info[11])
                            info[11] = re.sub("Company",'1',info[11])
                            info[11] = re.sub("",' ',info[11])
                        else:
                            info.append(" ")   
                    except:
                        pass

                    try:
                        info[12] = re.sub("Escrow Deposit","",info[12])
                    except:
                        pass
                    try:
                        info[13:35]=[]
                    except:
                        pass
                    try:
                        if len(info[12])>2:
                            info.append(info[12])
                        else:
                            info.append(info[9])
                    except:
                        pass
                    while len(info) < 11:
                        info.append("")
                    info.append("license number")
                            

                    l.info(info)
                    f.write("|".join(info) + "\n")
      
                except Exception, e:
                    l.error(str(e))

        except Exception, e:
            l.error(str(e))
            pass

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
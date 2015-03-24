import time, sys, requests, re, codecs, csv
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('gen.res_c_NMpsi', 'w', ['102', '32', '6', '21', '33', '37', '19', '13', 'volume', '0', '4', '36', '44', '35', 'qpcertificate no1', 'qpclassification1', 'qpattach date1', 'qpstatus1', '35', 'qpcertificate no2', 'qpclassification2', 'qpattach date2', 'qpstatus2'])
l = logger('gen.res_c_NMpsi')

def main():
    i = 0
    while i < 51500:
        try:
            i += 1 
            url = "https://public.psiexams.com/licensee/showBusinessLicensee.do?licenseId=%d&licenseApplicationId=173501" %i
            soup = BeautifulSoup(requests.get(url).content)
            tr = soup.find_all("tr")
            td = soup.find_all("td")
            fieldlabel = soup.find_all("fieldlabel")

            info = []

            info.append("License Number")
            info.append("Contractor")
            info.append(soup.find_all("td", {"class" : "fieldlabel"})[0].next)
            info.append(soup.find_all("td", {"class" : "fieldlabel"})[2].next)
            info.append(soup.find_all("td", {"class" : "fieldlabel"})[4].next)
            info.append(soup.find_all("td")[20].next)
            info.append(soup.find_all("td", {"class" : "fieldlabel"})[7].next)
            info.append(soup.find_all("td")[25].next)
            info.append(soup.find_all("td", {"class" : "fieldlabel"})[10].next)
            info.append(soup.find_all("td", {"class" : "fieldlabel"})[12].next)
            info.append(soup.find_all("td")[38].next)
            info.append(soup.find_all("td", {"class" : "fieldlabel"})[14].next)
            info.append(soup.find_all("td", {"class" : "fieldlabel"})[16].next)
            info.append(soup.find_all("td", {"class" : "fieldlabel"})[18].next)

            wr = (soup.find("tr", {"class" : "whiterow"})).find_all("tr")
            del(wr[0])
            for row in wr:
                for td in row.find_all("td"):
                    info.append(td.text)    
            del(info[10])
            f.write("|".join(info) + "\n")
            print(info)
        
        except Exception as e:
            l.error(str(e))
        
if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
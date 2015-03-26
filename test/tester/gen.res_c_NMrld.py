import time, sys, requests, re, codecs, csv
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('gen.res_c_NMpsi', 'w', [102, 32, 6, 21, 33, 37, 19, 13, 'volume', 0, 4, 36, 44, 35, 'qpcertificate no1', 'qpclassification1', 'qpattach date1', 'qpstatus1', 'qualifying_individual', 'qpcertificate no2', 'qpclassification2', 'qpattach date2', 'qpstatus2'])
l = logger('NMpsi')

def main():
    largeGap = 1000
    gap = 0
    i=0
    while True:
        try:
            l.debug(i)
            i+=1
            gap+=1
            if gap>largeGap*2 or i > 51481:
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
            l.info('\"' + "\",\"".join(data) + "\"\n")
            if gap>largeGap:
                largeGap = gap
        except Exception as e:
            l.error(str(e))

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()



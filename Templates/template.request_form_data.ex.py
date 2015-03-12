##################################################
# Output: arc_c_ARbar_date_000.txt
# Method: Requests, form data
##################################################

import codecs, re, requests, csv, time
from bs4 import BeautifulSoup

f = codecs.open("arc_c_ARbar_%s_000.txt" %(time.strftime("%Y%m%d")), "w", "utf-8")
headers = ["license_number", "company_flag", "address1", "city", "state", "zip", "status", "expiration_date", "number_type", "licensee_type_cd"]
f.write("|".join(headers) + "\"n")

###################################################

def log(status):
    feed = 'arc_c_ARbar_%s_000.txt' %(time.strftime('%Y%m%d'))
    l = codecs.open('log.csv', 'a')
    l.write(','.join([feed, str(time.strftime('%Y/%m/%d')), str(time.strftime('%H:%M:%S')), status]) + '\n')

def main():
    url = 'https://www.ark.org/asbalaid/index.php/arch/search_firm'
    soup = BeautifulSoup(requests.get(url).content)

    for option in soup.find('select', {'name' : 'state'}).find_all('option')[1:]:
        urlnext = 'https://www.ark.org/asbalaid/index.php/arch/search_firm?license_num=&name=&city=&state=' + option['value'] + '&submit=Search%21'
        soup = BeautifulSoup(requests.get(urlnext).content)
        for link in soup.find_all('a'):
            try:
                if 'details' in link['href']:
                    soup = BeautifulSoup(requests.get(link['href']).content)
                    info = []
                    for tr in soup.find("table", {"class" : "table"}, {"width" : "75%"}).find_all("tr"):
                        for td in tr.find_all("td")[1:]:
                            info.append(td.text)
                    info.append(soup.find_all("div", {"class" : "row-fluid"}, {"align" : "center"})[1].find("strong").text)
                    for link in soup.find_all("a"):
                        try:
                            if 'certificate_firm' in link['href']:
                                cert = BeautifulSoup(requests.get(link['href']).content)
                                info.append(cert.find_all("p", {"align" : "center"})[0].find("strong").text.replace("This individual registration expires on ", ""))
                        except Exception, e:
                            print str(e)
                    while len(info) < 8:
                        info.append("")
                    info.append("Certificate of Authorization Number")
                    info.append("Architectural Firm")
                    print info
                    f.write("|".join(info) + "\n")
            except Exception, e:
                print str(e)

		
if __name__ == '__main__':
        log('START')
        try:
            main()
            log('COMPLETE')
        except: log('ERROR')
        finally:
            f.close()

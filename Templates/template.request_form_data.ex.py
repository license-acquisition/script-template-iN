##################################################
# Output: arc_c_ARbar_date_000.txt
# Method: Requests, form data
##################################################

import requests
from bs4 import BeautifulSoup
from script_template import create_file


f = create_file('arc_c_ARbar', 'w', [21,6,0,4,36,44,37,13,102,32])
#headers = ["license_number", "company_flag", "address1", "city", "state", "zip", "status", "expiration_date", "number_type", "licensee_type_cd"]

###################################################

def main():
    url = 'https://www.ark.org/asbalaid/index.php/arch/search_firm'
    soup = BeautifulSoup(requests.get(url).content)

    for option in soup.find('select', {'name' : 'state'}).find_all('option')[1:]:
        urlnext = 'https://www.ark.org/asbalaid/index.php/arch/search_firm?license_num=&name=&city=&state=' + option['value'] + '&submit=Search%21'
        soup = BeautifulSoup(requests.get(urlnext).content)
        for link in soup.find_all('a'):
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

		
if __name__ == '__main__':
        try:
            main()
        except Exception, e:
            print str(e)
        finally:
            f.close()
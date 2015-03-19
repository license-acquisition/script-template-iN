##################################################
# Output: arc_c_ARbar_date_000.txt
# Method: Requests, form data
##################################################

import codecs, re, requests, csv, time
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('arc_c_ARbar', 'w', [21, 6, 0, 4, 36, 44, 36, 13, 102, 32])
l = logger('ARbar')
###################################################

def main():
    url = 'https://www.ark.org/asbalaid/index.php/arch/search_firm'
    soup = BeautifulSoup(requests.get(url).content)
    for option in soup.find('select', {'name' : 'state'}).find_all('option')[1:]:
        urlnext = 'https://www.ark.org/asbalaid/index.php/arch/search_firm?license_num=&name=&city=&state=' + option['value'] + '&submit=Search%21'
        soup = BeautifulSoup(requests.get(urlnext).content)
        for link in soup.find_all('a'):
            try:
                l.debug('Searching links')
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
                                l.info('found certification')
                                cert = BeautifulSoup(requests.get(link['href']).content)
                                info.append(cert.find_all("p", {"align" : "center"})[0].find("strong").text.replace("This individual registration expires on ", ""))
                        except Exception, e:
                            l.error(str(e))
                    while len(info) < 8:
                        info.append("")
                    info.append("Certificate of Authorization Number")
                    info.append("Architectural Firm")
                    l.info(info)
                    f.write("|".join(info) + "\n")
            except Exception, e:
                l.error(str(e))
        
		
if __name__ == '__main__':
    l.info('Starting script...')
    try:
        main()
        l.info('Complete!')
    except Exception as e:
        l.critical('Error in script')
        l.critical(str(e))
    finally:
        f.close()

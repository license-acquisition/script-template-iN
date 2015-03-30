import sys, re, requests, codecs, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from script_template import create_file, logger

f = create_file('pes_c_WIatc', 'w', [])
l = logger('pes_c_WIatc')
s = requests.Session()

def main():
        categories = []
        soup = BeautifulSoup(s.get('http://www.kellysolutions.com/WI/Business/searchbyCity.asp').content)
        for option in soup.find_all('option')[1:]:
                categories.append(option.text.strip())
        l.info(categories)
        for category in categories:
                soup = BeautifulSoup(s.get('http://www.kellysolutions.com/WI/Business/searchbyCity.asp?County=%s' %category).content)
                try:
                        for link in soup.find_all('a'):
                                if "showcoinfo" in link['href']:
                                        l.info(link['href'])
                                        soup2 = BeautifulSoup(s.get("http://www.kellysolutions.com/WI/Business/%s"%link['href']).content.replace("&nbsp;", " "))
                                        try:

                                                info = []
                                                for td in soup2.find_all('td', {'width': '78%'}):
                                                        info.append(td.text.replace("\r", " ").replace("\n", " "))
                                                
                                                info[5] = re.sub("  *", " ", info[5]).strip()
                                                info[5] = "\",\"".join(info[5].rsplit(" ", 2))

                                                l.info(info)
                                                f.write("|".join(info) + "\n")

                                        except Exception as e:
                                                l.error(str(e))
                except Exception as e:
                        l.debug('onto next category')
                        l.error(str(e))

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()

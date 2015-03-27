import sys, re, requests, codecs, csv
from bs4 import BeautifulSoup
from selenium import webdriver
from script_template import create_file, logger

f = create_file('pes_c_WIatc', 'w', [])
l = logger('pes_c_WIatc')

def main():
        categories = []
        soup = BeautifulSoup(requests.get('http://www.kellysolutions.com/WI/Business/searchbyCity.asp').content)
        for option in soup.find_all('option')[1:]:
                categories.append(option.text.strip())

        for category in categories:
                soup = BeautifulSoup(requests.get('http://www.kellysolutions.com/WI/Business/searchbyCity.asp?County=%s' %category).content)
                try:
                        for link in soup.find_all('a'):
                                #print link
                                if "showcoinfo" in link['href']:
                                        soup2 = BeautifulSoup(requests.get("http://www.kellysolutions.com/wv/Applicators/%s"%link['href']).content.replace("&nbsp;", " "))
                                        try:

                                                info = []
                                                info.append((re.search("NEB[0-9]{6}",soup2.text).group()))
                                                info.append((re.search("\d{1,2}[/]\d{1,2}[/]\d{4}",soup2.text).group()))
                                                info.append(soup2.find_all("p", {"style" : "margin-top: 0; margin-bottom: 0"})[4].text.replace("\r", "").replace("\n", ""))
                                                info.append(soup2.find_all("td", {"width" : "82%"})[0].text.replace("\r", " ").replace("\n", " "))
                                                info.append(soup2.find_all("td", {"width" : "82%"})[1].text.replace("\r", " ").replace("\n", " "))
                                                info.append(soup2.find_all("td", {"width" : "82%"})[2].text.replace("\r", " ").replace("\n", " "))
                                                info.append(soup2.find_all("td", {"width" : "82%"})[3].text.replace("\r", " ").replace("\n", " "))
                                                info.append(soup2.find_all("td", {"width" : "77%"})[0].text.strip().replace("\r", " ").replace("\n", "\",\""))
                                                
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

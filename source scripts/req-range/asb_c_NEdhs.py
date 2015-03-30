import sys
import requests
from bs4 import BeautifulSoup
import codecs, time
import re
import csv
from script_template import create_file, logger

f = create_file('asb_c_NEdhs', 'w', ['7', '34', 'Address/City/State/Zip', '33', '32', '22', '21', '19'])
l = logger('asb_c_NEdhs')
s = requests.Session()

def main():
        url = 'http://www.nebraska.gov/LISSearch/search.cgi'
        s.get(url)
        for i in range(1, 10000): #10000
                try:
                        url = 'http://www.nebraska.gov/LISSearch/search.cgi?city=&zip=&profession=10&county=&lname=&licnum=BEL-%s&mode=list&fname=&licstat=ALL&stype=E' %i
                        soup = BeautifulSoup(s.get(url).content)
                        for link in soup.find_all("a"):
                                try:
                                        print link['href']
                                        if "mode=details" in link['href']:
                                                l.info(link['href'])
                                                soup = BeautifulSoup(s.get("http://www.nebraska.gov/LISSearch/%s"%link['href']).content)
                                                info = []
                                                for j in soup.find_all("div", {"class" : "fieldValue"}):
                                                        info.append(j.text)
                                                f.write("|".join(info) + "\n")     
                                                l.info(info)
                                except Exception, e:
                                        l.error(str(i) + ' - ' + str(e))
                                        pass
                except Exception, e:
                        l.error(str(e))
                        pass

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e: l.critical(str(e))
        finally:
                f.close()

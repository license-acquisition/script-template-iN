import sys, re, requests, codecs, csv, time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
from glob import glob
from string import ascii_letters, digits
from script_template import create_file, logger

f = create_file('pes_c_CTdee', 'w', ['6', '12', '0', '13', '32'])
l = logger('pes_c_CTdee')
g = codecs.open('pes_c_CTdee_links.csv', 'w', 'utf-8')
s = requests.Session()

def main():
    url = "http://www.kellysolutions.com/CT/Business/searchbyCategory.asp"
    categories = []
    soup = BeautifulSoup(s.get(url).content)
    for option in soup.find_all('option'):
            categories.append(option.text[:option.text.find('-')].strip())
    l.info(categories)
    for category in categories:
            try:
                    url = 'http://www.kellysolutions.com/CT/Business/searchbyCategory.asp?Cat1=%s' %category
                    soup = BeautifulSoup(s.post(url).content)
                    for link in soup.find_all('a'):
                            if "showcoinfo" in link['href']:
                                    l.info(link['href'])
                                    g.write("http://www.kellysolutions.com/CT/Business/%s\n"%link['href'])
            except Exception as e:
                    l.error(str(e))
                    l.error('Next category')
    g.close()                

    for line in open("pes_c_CTdee_links.csv", "r"):
            soup2 = BeautifulSoup(requests.get(line.strip()).content.replace("&nbsp;", " "))
            for bold in soup2.find_all('b'):
                    bold.decompose()
            try:
                    info = []       
                    ps = soup2.find_all('p')
                    for p in ps[1:-4]:
                            
                            info.append(p.text.replace("\r", "").replace("\n", "").strip())
                    try:
                            del(info[0])
                            del(info[0])
                            del(info[1])
                            del(info[1])
                            del(info[2])
                            del(info[2])
                            del(info[3])
                            del(info[3])
                    except:
                            pass
                    info.insert(0,"1")
                    
                    l.info(info)
                    f.write('|'.join(info) + '\n')

            except Exception, e:      
                    l.error(str(e))
                        
if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()

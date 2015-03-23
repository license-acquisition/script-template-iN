import sys, re, requests, codecs, csv, time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
from glob import glob
from string import ascii_letters, digits
start=time.time()

f = codecs.open('pes_c_CTdee_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ["company_flag","entity_name","address1","expiration_date","licensee_type_cd"]
f.write('|'.join(headers) + '\n')

g = open("pes_c_CTdee_links.txt", "w")

url = "http://www.kellysolutions.com/CT/Business/searchbyCategory.asp"
categories = []
soup = soupify(requests.get(url).content)
for option in soup.find_all('option'):
        categories.append(option.text[:option.text.find('-')].strip())
for category in categories:
        try:
                url = 'http://www.kellysolutions.com/CT/Business/searchbyCategory.asp?Cat1=%s' %category
                soup = soupify(requests.get(url))
                for link in soup.find_all('a'):
                        #print link
                        if "showcoinfo" in link['href']:
                                g.write("http://www.kellysolutions.com/CT/Business/%s\n"%link['href'])
                                
                browser.find_element_by_css_selector("input[value='  >   ']").click()
        except:
                print "Next list %d"%j
                j=j+1
                print j
                break

for line in open("pes_c_CTdee_links.txt", "r"):
        soup2 = BeautifulSoup(requests.get(line.strip()).content.replace("&nbsp;", " "))
        for bold in soup2.find_all('b'):
                bold.decompose()
        try:
                data = []       
                ps = soup2.find_all('p')
                for p in ps[1:-4]:
                        
                        data.append(p.text.replace("\r", "").replace("\n", "").strip())
                try:
                        del(data[0])
                        del(data[0])
                        del(data[1])
                        del(data[1])
                        del(data[2])
                        del(data[2])
                        del(data[3])
                        del(data[3])
                except:
                        pass
                data.insert(0,"1")
                
                print('\"' + "\",\"".join(data) + "\"\n")
                f.write('\"' + "\",\"".join(data) + "\"\n")

        except Exception, e:
                print(data)             
                print str(e)
                        

f.close()

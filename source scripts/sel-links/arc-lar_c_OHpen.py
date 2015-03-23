from selenium import webdriver
import codecs
from itertools import product
from string import ascii_uppercase
from datetime import date
import requests
from bs4 import BeautifulSoup
import codecs
import re, time
year = date.today().year
month = date.today().month
day = date.today().day
'''
keywords = [''.join(i) for i in product(ascii_uppercase, repeat =2)]
l=codecs.open("OH_arc-lar_Links.csv","w","utf-8")
browser  = webdriver.Chrome()
browser.get("https://license.ohio.gov/Lookup/")
browser.find_element_by_css_selector("#iform > table > tbody > tr > td > table:nth-child(5) > tbody > tr:nth-child(1) > td:nth-child(2) > select > option:nth-child(3)").click()
for x in keywords:
    try:
        search = browser.find_element_by_css_selector("#iform > table > tbody > tr > td > table:nth-child(6) > tbody > tr:nth-child(3) > td:nth-child(2) > input[type='text']")
        search.clear()
        search.send_keys("%s"%x)
        browser.find_element_by_css_selector("#iform > table > tbody > tr > td > table:nth-child(6) > tbody > tr:nth-child(9) > td:nth-child(2) > input[type='submit']:nth-child(1)").click()
        for a in browser.find_elements_by_css_selector("#iform > table > tbody > tr > td > table:nth-child(7) > tbody > tr > td:nth-child(1) > a"):
            info = []
            info.append((a.get_attribute('href')))
            print ("\"" + "\"\n\"".join(info) + "\"\n")
            l.write("\"" + "\"\n\"".join(info) + "\"\n")
    except Exception, e:
        print str(e)
l.close()
browser.close()
browser.quit()
'''
f = codecs.open('arc-lar_c_OHpen_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')
f.write("company_flag|number_type|license_type_cd|license2|entity_name|address1|city|state|zip|license_number|licensetype|first_issue_date|expiration_date|status|disciplinary_status|primary_specialty\n")
s = requests.session()
#browser.get("https://license.ohio.gov/Lookup/")
for line in codecs.open("OH_arc-lar_Links.csv","r","utf-8"):
    try:
        quotes = "%s" %line
        link = quotes.replace("\"","")
        link_mod = link.replace("ivisionIdnt=100","ivisionIdnt=89")
        licenseno = re.search("Idnt=(.*?)&D",link_mod).group(1)
        print licenseno
        print link_mod
        #browser.get(link)
        source = s.get(link_mod)
        
        soup = BeautifulSoup(source.content)
        
        #soup = BeautifulSoup(browser.page_source)
        info = []
        info.append("1")
        
        info.append("License Number")
        
        info.append("Archtecture")
        
        info.append(licenseno)
        
        table = soup.find("table",{"border":"1"})
        td = soup.findAll('td')
        ok = soup.findAll("td",{"bgcolor":"#FFFFFF"})
        info.append(ok[1].text.strip().replace(u'\xa0',u''))
        addy = ok[3].text.replace(u'\xa0',u'')
        #info.append(addy)
        sub = re.sub("\w[A-Za-z ]+, [A-Z]{2}","",addy)
        ugh = re.sub("(\d{5})","",sub)
        info.append(re.sub("(-)+[0-9]{4,5}","",ugh).replace("United States of America","").strip())
       
        #info.append(re.sub("\s*"," ",clean))
        addstate = re.search("\w[A-Za-z ]+, [A-Z]{2}",addy).group()
        info.append(re.sub(", [A-Z]{2}","",addstate) or '')
        info.append(re.search("[A-Z]{2}",addstate).group() or '')
        info.append(re.search("\d{5}",addy).group() or '')
        info.append(ok[4].text.strip().replace(u'\xa0',u''))
        info.append(ok[5].text.strip().replace(u'\xa0',u''))
        info.append(ok[6].text.strip().replace(u'\xa0',u''))
        info.append(ok[7].text.strip().replace(u'\xa0',u''))
        print 7
        info.append(ok[8].text.strip().replace(u'\xa0',u''))
        try:
            source2 = s.get(link)
            soup2 = BeautifulSoup(source2.content)
            disc = soup2.findAll("td",{"bgcolor":"#FFFFFF"})
            info.append(disc[9].text.strip())
            info.append(disc[10].text.strip())
            print 8
        except Exception, e:
            print e
        print("\"" + "\",\"".join(info) + "\"\n")
        f.write("\"" + "\"|\"".join(info) + "\"\n")
    except Exception, e:
        print str(e)
        #print %s %line
f.close()


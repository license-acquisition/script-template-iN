from selenium import webdriver
import codecs
from itertools import product
from string import ascii_uppercase
from datetime import date
import requests
from bs4 import BeautifulSoup
import codecs
import re, time
from glob import glob
from script_template import create_file, logger

f = create_file('arc-lar_c_OHpen', 'w', ['6', '102', '32', '27', '12', '0', '4', '36', '44', '21', 'license_type', '19', '13', '37', '62', '78'])
l = logger('arc-lar_c_OHpen')
g = codecs.open("arc-lar_c_OHpen_links.csv","w","utf-8")
driver  = webdriver.PhantomJS()

def main():
    keywords = [''.join(i) for i in product(ascii_uppercase, repeat =2)]

    driver.get("https://license.ohio.gov/Lookup/")
    driver.find_element_by_css_selector("#iform > table > tbody > tr > td > table:nth-child(5) > tbody > tr:nth-child(1) > td:nth-child(2) > select > option:nth-child(3)").click()
    for word in keywords:
        try:
            search = driver.find_element_by_css_selector("#iform > table > tbody > tr > td > table:nth-child(6) > tbody > tr:nth-child(3) > td:nth-child(2) > input[type='text']")
            search.clear()
            search.send_keys("%s"%word)
            driver.find_element_by_css_selector("#iform > table > tbody > tr > td > table:nth-child(6) > tbody > tr:nth-child(9) > td:nth-child(2) > input[type='submit']:nth-child(1)").click()
            for a in driver.find_elements_by_css_selector("#iform > table > tbody > tr > td > table:nth-child(7) > tbody > tr > td:nth-child(1) > a"):
                info = []
                info.append((a.get_attribute('href')))
                l.info(info)
                l.write("\"" + "\"\n\"".join(info) + "\"\n")
        except Exception, e:
            l.error(str(e))

    g.close()
    driver.quit()

    s = requests.session()
    #driver.get("https://license.ohio.gov/Lookup/")
    for line in codecs.open("arc-lar_c_OHpen_links.csv","r","utf-8"):
        try:
            quotes = "%s" %line
            link = quotes.replace("\"","")
            link_mod = link.replace("ivisionIdnt=100","ivisionIdnt=89")
            licenseno = re.search("Idnt=(.*?)&D",link_mod).group(1)
            l.info(licenseno)
            l.info(link_mod)
            #driver.get(link)
            source = s.get(link_mod)
            
            soup = BeautifulSoup(source.content)
            
            #soup = BeautifulSoup(driver.page_source)
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
          
            info.append(ok[8].text.strip().replace(u'\xa0',u''))
            try:
                source2 = s.get(link)
                soup2 = BeautifulSoup(source2.content)
                disc = soup2.findAll("td",{"bgcolor":"#FFFFFF"})
                info.append(disc[9].text.strip())
                info.append(disc[10].text.strip())
                
            except Exception, e:
                l.error(str(e))
            l.info(info)
            f.write("\"" + "\"|\"".join(info) + "\"\n")
        except Exception, e:
            l.error(str(e))
            #print %s %line


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
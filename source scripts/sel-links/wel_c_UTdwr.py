from selenium import webdriver
import codecs
from bs4 import BeautifulSoup
import requests
import re

browser = webdriver.PhantomJS()
url = "http://www.waterrights.utah.gov/cgi-bin/drilview.exe"
browser.get(url)
browser.find_element_by_css_selector("body > form > pre > select > option:nth-child(7)").click()
f=codecs.open("UtahWell.csv","w","utf-8")
for a in browser.find_elements_by_css_selector("body > form > pre > p:nth-child(3) > a"):
    info = []
    info.append((a.get_attribute('href')))
    print ("\"" + "\"\n\"".join(info) + "\"\n")
    f.write("\"" + "\"\n\"".join(info) + "\"\n")
f.close()

#from selenium import webdriver

f=codecs.open("wel_c_UTdwr_20140801_000.csv","w","utf-8")
#s = requests.session()
browser = webdriver.PhantomJS()
import re
for line in codecs.open("UtahWell.csv"):
    try:
        asdf = "%s" %line
        link = asdf.replace("\"","")
        #source = s.get(link)
        browser.get(link)
        info = []
        name = str(browser.find_element_by_css_selector("body > pre").text)
        name = re.sub("\s\s*"," ",name)
        company = re.search("Company Name: (.*?) License Number:",name).group().replace("Company Name: ","").replace("License Number:","").strip()
        info.append(company)
        number = re.search("Number: (.*?)\s",name).group().replace("Number:","").strip()
        info.append(number)
        person = re.search("Licensee: (.*?) Bus Phone:",name).group()
        info.append(person)
        info.append(re.search("Bus Phone: (.*?) Licenses:",name).group())
        info.append(re.search("Licenses:(.*)",name).group())
        #info.append(re.search("Drilling Methods: (.*?) Driller Activities",strname).group())
        print("\"" + "\",\"".join(info) + "\"\n")
        f.write("\"" + "\",\"".join(info) + "\"\n")
        #print browser.current_url
    except Exception, e:
        print str(e)

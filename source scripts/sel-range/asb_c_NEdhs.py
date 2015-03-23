import sys
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import codecs, time
import re
import csv


f = codecs.open('asb_c_NEdhs_%s_000.csv'%time.strftime('%Y%m%d'), 'w', 'utf-8')

browser = webdriver.PhantomJS()
for i in range(1, 10000):
        try:
                browser.get("http://www.nebraska.gov/LISSearch/search.cgi?new=1&stype=I")
                browser.find_elements_by_css_selector("input")[1].click()
                time.sleep(.2)
                browser.find_elements_by_css_selector("input")[5].click()
                browser.find_elements_by_css_selector("option")[2].click()
                browser.find_element_by_name("licnum").send_keys("BEL-%s" %str(i))
                browser.find_element_by_css_selector("input[value='Search Entities']").click()
                soup = BeautifulSoup(browser.page_source)


                for link in soup.findAll("a"):
                        try:
                                #print link['href']
                                if "mode=details" in link['href']:
                                        soup = BeautifulSoup(requests.get("http://www.nebraska.gov/LISSearch/%s"%link['href']).content)
                                        data = []
                                        for j in soup.find_all("div", {"class" : "fieldValue"}):
                                                data.append(j.text)
                                        f.write('\"' + "\"|\"".join(data) + "\"\n")     
                                        print ('\"' + '\"\n\"'.join(data))
                                        #print soup.text
                        except Exception, e:
                                print str(e)
                                pass
        except Exception, e:
                print str(e)
                pass
f.close()
browser.close()
browser.quit()

"""for i in range(165409, 900000, 500):

    try:
        url = "http://www.nebraska.gov/LISSearch/search.cgi?mode=details&lid=%d&stype=I" %i

        page = requests.get(url)
        soup = BeautifulSoup(page.content)
        div = soup.find_all("div")
        fieldlabel = soup.find_all("fieldValue")

        data = []
        data.append(str(i))
        for j in soup.find_all("div", {"class" : "fieldValue"}):
                data.append(j.text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[0].text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[1].text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[2].text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[3].next.text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[4].next.text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[5].next.text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[6].next.text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[7].next.text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[8].next.text)
        #data.append(soup.find_all("div", {"class" : "fieldValue"})[9].next.text)

        f.write('\"' + "\",\"".join(data) + "\"\n")     
        print ('\"' + '\"\n\"'.join(data))


    except Exception as e:
    
        print str(e)

f.close()"""

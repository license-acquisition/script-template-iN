import sys
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import codecs, time
import re
import csv


f = codecs.open('led_c_NEdhs_%s_000.csv' % time.strftime('%Y%m%d'), 'w', 'utf-8')

browser = webdriver.PhantomJS()
browser.get("http://www.nebraska.gov/LISSearch/search.cgi?new=1&stype=I")
for i in range(1, 300):
        try:
                
                browser.find_elements_by_css_selector("input")[1].click()
                time.sleep(.2)
                browser.find_elements_by_css_selector("input")[5].click()
                browser.find_elements_by_css_selector("option")[11].click()
                if i < 10:
                        browser.find_element_by_name("licnum").send_keys("BEC-00%s" %str(i))
                elif i < 100:
                        browser.find_element_by_name("licnum").send_keys("BEC-0%s" %str(i))
                else:
                        browser.find_element_by_name("licnum").send_keys("BEC-%s" %str(i))
                browser.find_element_by_css_selector("input[value='Search Entities']").click()
                soup = BeautifulSoup(browser.page_source)
                browser.back()

                for link in soup.findAll("a"):
                        try:
                                #print link['href']
                                if "mode=details" in link['href']:
                                        soup = BeautifulSoup(requests.get("http://www.nebraska.gov/LISSearch/%s"%link['href']).content)
                                        data = []
                                        for j in soup.find_all("div", {"class" : "fieldValue"}):
                                                data.append(j.text)
                                        f.write('\"' + "\",\"".join(data) + "\"\n")     
                                        print ('\"' + '\"\n\"'.join(data))
                                        #print soup.text
                        except:
                                pass
        except:
                pass

f.close()
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

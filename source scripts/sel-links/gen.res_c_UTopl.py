from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import csv
import re
import codecs
from selenium.webdriver.support.ui import Select

count = 1
stamp = time.strftime("%Y%m%d")
url = 'https://secure.utah.gov/llv/search/'
browser = webdriver.Chrome()
l = codecs.open("UT_links.csv","w","utf-8")

browser.get('https://secure.utah.gov/llv/search/index.html')
browser.find_element_by_css_selector("#professions3").click() # Architect
browser.find_element_by_css_selector("#professions6").click() # Building Inspector
browser.find_element_by_css_selector("#professions7").click() # Burglar Alarm
browser.find_element_by_css_selector("#professions10").click() # Contractor
browser.find_element_by_css_selector("#professions20").click() # Electrician
browser.find_element_by_css_selector("#professions24").click() #Factory Built Housing
browser.find_element_by_css_selector("#professions21").click() # Engineer/Land Surveyor
browser.find_element_by_css_selector("#professions28").click() # Handyman
browser.find_element_by_css_selector("#professions22").click() # Elevator Mechanic
browser.find_element_by_css_selector("#professions32").click() # Landscape Architect
browser.find_element_by_css_selector("#professions52").click() # Plumber
browser.find_element_by_css_selector("#professions59").click() # Security Companies & Guards
browser.find_element_by_xpath("//*[@id='command']/fieldset[3]/p[3]/input[1]").click()

while True:
    soup = BeautifulSoup(browser.page_source)
    links = soup.find_all("a")
    the_links = []
    i = 0
    for link in links:
        if i > 11 and i%2 == 0:
            the_links.append(url + re.split('"',re.split('href="',str(link))[1])[0])
            print url + re.split('"',re.split('href="',str(link))[1])[0]
            l.write("\"" + "\"\n\"".join(the_links) + "\"\n")
        i = i + 1
    browser.find_element_by_css_selector("#pagination-next").click()
l.close()
ft = codecs.open("arc-ele-eng-gen.res-hom-lar-plu-sec-sur_i_UTopl_%s_000.csv"%stamp, "w", "utf-8")
ft.write("company_name,city,state,zipcode,profession,licensee_type_cd,license_number,obtby,status,issdate,expire_date,agency,docket,company_flag\n")
s = requests.session()
browser = webdriver.Chrome()
s.get("https://secure.utah.gov/llv/search/detail.html?license_id=4893075")
for line in codecs.open("UT_links.csv","r","utf-8"):
    try:
            x = line.replace("\"","")
            print x
            browser.get(x)
            soup = BeautifulSoup(browser.page_source)
            info = []
            td = soup.findAll("td")
            name = td[1].text.strip()
            address = td[3].text
            zipcode = re.search("[0-9]{5}",address).group()
            statesplit = address.rsplit(",",2)[1]
            state = re.search("[A-Z]{2}",statesplit).group()
            city = address.split(",",1)[0].strip()
            profession = td[5].text.strip()
            lictype = td[7].text.strip()
            licnumb1 = td[9].text.strip()
            if re.match("[A-Z]",licnumb1):
                licnumb = td[11].text.strip()
            if re.match("[0-9]",licnumb1):
                licnumb = td[9].text.strip()
            obtby = td[11].text.strip()
            if re.match("[0-9]",obtby):
                obtby = td[13].text.strip()
            licstat = td[13].text.strip()
            issdate = td[15].text.strip()
            if re.match("[A-Z]",issdate):
                issdate = td[17].text.strip()
            if issdate == "":
                issdate = " "
            expdate = td[17].text.strip()
            if re.match("[A-Z]",expdate):
                expdate = td[19].text.strip()
            if expdate == "":
                expdate = " "
            agency = td[19].text.strip()
            if re.match("[0-9]",agency):
                agency = td[21].text.strip(0)
            if agency == "":
                agency = " "
            docket = td[21].text.strip()
            if docket == "":
                docket = " "
            info.append(name)
            info.append(city)
            info.append(state)
            info.append(zipcode)
            info.append(profession)
            info.append(lictype)
            info.append(licnumb1)
            info.append(obtby)
            info.append(licstat)
            info.append(issdate)
            info.append(expdate)
            info.append(agency)
            info.append(docket)
            info.append(1)
            print name, city, state, zipcode, profession, lictype, licnumb1, obtby, licstat, issdate, expdate, agency, docket
            #f.writerow([company_name,city,state,zip,profession,licensee_type_cd, license_number,obtby,status,first_issue_date,expire_date,agency,docket])
            ft.write("\"" + "\",\"".join(info) + "\"\n")
    except Exception,e:
        print str(e)
        count = count + 1
        print count

f.close()
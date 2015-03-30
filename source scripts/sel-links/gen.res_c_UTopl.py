from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import time
import csv
import re
import codecs
from selenium.webdriver.support.ui import Select
from script_template import create_file, logger

f = create_file('gen.res_c_UTopl', 'w', ['7', '4', '36', '44', 'profession', '32', '21', 'obtby', '37', '19', '13', 'agency', 'docket', '6'])
l = logger('gen.res_c_UTopl')
g = codecs.open('gen.res_c_UTopl_links.csv', 'w', 'utf-8')
driver = webdriver.PhantomJS()
s = requests.Session()

def main():
    count = 1
    url = 'https://secure.utah.gov/llv/search/'
    driver.get('https://secure.utah.gov/llv/search/index.html')
    driver.find_element_by_css_selector("#item6").click() # Architect
    driver.find_element_by_css_selector("#item12").click() # Building Inspector
    driver.find_element_by_css_selector("#item15").click() # Burglar Alarm
    driver.find_element_by_css_selector("#item29").click() # Contractor
    driver.find_element_by_css_selector("#item173").click() # Electrician
    driver.find_element_by_css_selector("#item188").click() #Factory Built Housing
    driver.find_element_by_css_selector("#item181").click() # Engineer/Land Surveyor
    #driver.find_element_by_css_selector("#item").click() # Handyman
    driver.find_element_by_css_selector("#item179").click() # Elevator Mechanic
    driver.find_element_by_css_selector("#item210").click() # Landscape Architect
    driver.find_element_by_css_selector("#item325").click() # Plumber
    driver.find_element_by_css_selector("#item360").click() # Security Companies & Guards
    driver.find_element_by_xpath("//*[@id='command']/fieldset[3]/p/input[1]").click()

    while True:
        soup = BeautifulSoup(driver.page_source)
        links = soup.find_all("a")
        the_links = []
        i = 0
        for link in links:
            if i > 11 and i%2 == 0:
                the_links.append(url + re.split('"',re.split('href="',str(link))[1])[0])
                l.info(url + re.split('"',re.split('href="',str(link))[1])[0])
                g.write("\"" + "\"\n\"".join(the_links) + "\"\n")
            i += 1
        driver.find_element_by_css_selector("#pagination-next").click()
    g.close()

    s.get("https://secure.utah.gov/llv/search/detail.html?license_id=4893075")
    for line in open('gen.res_c_UTopl_links.csv', 'r'):
        try:
                x = line.replace("\"","")
                l.debug(x)
                driver.get(x)
                soup = BeautifulSoup(driver.page_source)
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
                for data in [name, city, state, zipcode, profession, lictype, licnumb1, obtby, licstat, issdate, expdate, agency, docket, 1]:
                    info.append(data)
                l.info(info)
                ft.write("|".join(info) + "\n")
        except Exception,e:
            l.error(str(e))
            count += 1

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
from selenium import webdriver
import codecs
from bs4 import BeautifulSoup
import requests
import re
from script_template import create_file, logger

f = create_file('wel_c_UTdwr', 'w', [])
l = logger('wel_c_UTdwr')
g = codecs.open('wel_c_UTdwr_links.csv', 'w', 'utf-8')
driver = webdriver.PhantomJS()

def main():
    url = "http://www.waterrights.utah.gov/cgi-bin/drilview.exe"
    driver.get(url)
    driver.find_element_by_css_selector("body > form > pre > select > option:nth-child(7)").click()
    for a in driver.find_elements_by_css_selector("body > form > pre > p:nth-child(3) > a"):
        info = []
        info.append((a.get_attribute('href')))
        l.info(info)
        g.write("\"" + "\"\n\"".join(info) + "\"\n")
    g.close()

    for line in codecs.open("wel_c_UTdwr_links.csv"):
        try:
            asdf = "%s" %line
            link = asdf.replace("\"","")
            #source = s.get(link)
            driver.get(link)
            info = []
            name = str(driver.find_element_by_css_selector("body > pre").text)
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
            l.info(info)
            f.write("|".join(info) + "\n")
        except Exception, e:
            l.error(str(e)

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
import codecs, re, csv, time
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('wel_c_NYdec', 'w', ['6', '0', '4', '36', '44', '33', '21', '102', '32'])
l = logger('wel_c_NYdec')
driver = webdriver.PhantomJS()

def main():
        for i in range(2, 18):
                driver.get("http://www.dec.ny.gov/cfmx/extapps/WaterWell/index.cfm")
                driver.find_element_by_css_selector("input[value='Select County']").click()
                driver.find_element_by_css_selector("#activity_code > option:nth-child(%d)"%i).click()
                driver.find_element_by_css_selector("input[value='Start']").click()
                while True: #avoid while true if you can. 
                        try:
                                soup = BeautifulSoup(driver.page_source)
                                for tr in soup.find_all("table")[0].find_all("tr")[3:-2]:
                                        info = []
                                        for td in tr.find_all("td"):
                                                info.append(td.text.strip())    
                                        info.append("Registration Number")
                                        info.append("Water Well Contractor")
                                        f.write("|".join(info) + "\n")
                                        l.info('|'.join(info) + "\n")
                                        driver.find_element_by_partial_link_text("Next").click()
                        except:
                                #if next doesn't exist, break the while loop
                                l.debug('Done looking through pages')
                                break

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception, e:
                l.critical(str(e))
        finally:
                driver.quit()
                f.close()

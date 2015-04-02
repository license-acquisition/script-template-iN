import sys
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import codecs, time
import re
import csv
from script_template import create_file, logger

f = create_file('led_c_NEdhs', 'w', [])
l = logger('led_c_NEdhs')
driver = webdriver.PhantomJS()

def main():
    driver.get("http://www.nebraska.gov/LISSearch/search.cgi?new=1&stype=I")
    for i in range(1, 300):
            try:
                    
                    driver.find_elements_by_css_selector("input")[1].click()
                    time.sleep(.2)
                    driver.find_elements_by_css_selector("input")[5].click()
                    driver.find_elements_by_css_selector("option")[11].click()
                    if i < 10:
                            driver.find_element_by_name("licnum").send_keys("BEC-00%s" %str(i))
                    elif i < 100:
                            driver.find_element_by_name("licnum").send_keys("BEC-0%s" %str(i))
                    else:
                            driver.find_element_by_name("licnum").send_keys("BEC-%s" %str(i))
                    driver.find_element_by_css_selector("input[value='Search Entities']").click()
                    soup = BeautifulSoup(driver.page_source)
                    driver.back()

                    for link in soup.findAll("a"):
                            try:
                                    if "mode=details" in link['href']:
                                            soup = BeautifulSoup(requests.get("http://www.nebraska.gov/LISSearch/%s"%link['href']).content)
                                            info = []
                                            for j in soup.find_all("div", {"class" : "fieldValue"}):
                                                    info.append(j.text)
                                            f.write('|'.join(info) + '\n')     
                                            l.info(info)
                            except:
                                    pass
            except Exception as e:
                    l.error(str(e))

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()
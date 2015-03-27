import sys
import re
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from script_template import create_file, logger

f = create_file('ele-hva-plu_c_NHoli', 'w', ['6', '12', '21', 'profession', '32', '37', '19', '13'])
l = logger('ele-hva-plu_c_NHoli')
driver = webdriver.PhantomJS()

def main():
	protype = ['Electricians','Building Trades']
	links = []
	fail = 0
	for x in protype:
		driver.get('http://nhlicenses.nh.gov/mylicense%20verification/Search.aspx?facility=Y')
		Select(driver.find_element_by_id("t_web_lookup__profession_name")).select_by_visible_text("%s"%x)
		driver.find_element_by_id("sch_button").click()
		time.sleep(1)
		i=1
		#datagrid_results > tbody > tr:nth-child(3) > td > font > a:nth-child(9)
		while fail == 0:
			try:
				if fail == 1:
					break
				driver.find_element_by_partial_link_text("%s"%i).click()
				time.sleep(3)
				for link in BeautifulSoup(driver.page_source).findAll("a"):
					if "Details" in link['href']:
						l.info('found link: ' + link['href'])
						links.append(link['href'])
					else:
						pass
				i+=1
			except Exception as e:
				l.error(str(e))
				fail = 1
		
	for url in links:
	    try:
	        url_string = "http://nhlicenses.nh.gov/mylicense verification/" + "%s"%url
	        soup = BeautifulSoup(requests.get(url_string).content)
	        info = []
	        info.append("1")
	        info.append(soup.findAll("span", {"id" : "_ctl14__ctl1_full_name"})[0].next)
	        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_license_no"})[0].next)
	        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_profession_id"})[0].next)
	        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_license_type"})[0].next)
	        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_sec_lic_status"})[0].next)
	        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_issue_date"})[0].next)
	        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_expiration_date"})[0].next)
	        f.write("|".join(data) + "\n")
	        l.info(info)
	    except:
	    	continue

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
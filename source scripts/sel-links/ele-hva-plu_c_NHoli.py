import sys
import re
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
f=open("ele_plu_c_NHoli_%s.csv"%(time.strftime("%Y%m%d")),"a")
browser = webdriver.PhantomJS()
f.write("company_flag,entity_name,license_number,profession,licensee_type_cd,status,first_issued_date,expiration_date\n")
protype = ['Electricians','Building Trades']
urls = []
fail = 0
for x in protype:
	browser.get('http://nhlicenses.nh.gov/mylicense%20verification/Search.aspx?facility=Y')
	Select(browser.find_element_by_id("t_web_lookup__profession_name")).select_by_visible_text("%s"%x)
	browser.find_element_by_id("sch_button").click()
	time.sleep(1)
	i=1
	#datagrid_results > tbody > tr:nth-child(3) > td > font > a:nth-child(9)
	while fail == 0:
		try:
			if fail == 1:
				break
			browser.find_element_by_partial_link_text("%s"%i).click()
			time.sleep(3)
			for link in BeautifulSoup(browser.page_source).findAll("a"):
				if "Details" in link['href']:
					print link['href']
					urls.append(link['href'])
				else:
					pass
			i+=1
			print i
		except Exception:
			fail = 1
	
print browser.current_url
for url in urls:
    try:
        url_string = "http://nhlicenses.nh.gov/mylicense verification/" + "%s"%url
        browser.get(url_string)
        c = browser.page_source
        soup = BeautifulSoup(c)
        currenturl = browser.current_url
        info = []
        info.append("1")
        info.append(soup.findAll("span", {"id" : "_ctl14__ctl1_full_name"})[0].next)
        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_license_no"})[0].next)
        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_profession_id"})[0].next)
        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_license_type"})[0].next)
        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_sec_lic_status"})[0].next)
        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_issue_date"})[0].next)
        info.append(soup.findAll("span", {"id" : "_ctl20__ctl1_expiration_date"})[0].next)
        f.write('\"' + "\",\"".join(data) + "\"\n")
        print('\"' + "\",\"".join(data) + "\"\n")
    except:
    	continue

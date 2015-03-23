# Kyle

# Grabbing URLs

import time, re, codecs
from glob import glob
from selenium import webdriver
from bs4 import BeautifulSoup
browser = webdriver.PhantomJS()
f = open("ALpestURLs2.txt", "w")
# Private or Commercial
browser.get("http://agi-app.alabama.gov/Commercial.aspx")
browser.find_element_by_id("ctl00_ContentPlaceHolder2_btnSearch").click()
i = 2
while i < 531:
	for link in BeautifulSoup(browser.page_source).findAll("a"):
		try:
			if "Details" in link['href']:
				f.write(link['href'] + "\n")
		except:
			pass
	if i == 11:
		browser.find_element_by_link_text("...").click()
	elif i % 10 == 1:
		browser.find_elements_by_link_text("...")[1].click()
	else:
		browser.find_element_by_link_text("%s"%i).click()
	i += 1
	print i
	
print 'Done'

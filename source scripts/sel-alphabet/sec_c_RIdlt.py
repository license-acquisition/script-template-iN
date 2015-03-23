# only works with ie driver or firefox driver
from bs4 import BeautifulSoup
from selenium import webdriver
import string
from datetime import date
import re, time
import codecs
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open("sec_c_RIdlt_%s%s%s_000.csv" %(str(year), str(month).zfill(2), str(day).zfill(2)),"w","utf-8")
f.write("license_type_cd,disciplinary_string,license_number,expiration_date,last_renew_date,entity_name,address1,city,state,zip,phone,DBA,qualifying_individual,middle,last,status,company_flag\n")
#f = open("RIalarm.csv", "w")
#DGalarmco$ctl10$ctl00
browser = webdriver.Firefox()
browser.get("http://www.dlt.ri.gov/profregsonline/PROLentree1.aspx")
browser.find_elements_by_tag_name("input")[7].click()
time.sleep(3)
for i in string.ascii_lowercase:
	browser.find_element_by_id("txtLastName").send_keys("%s"%i)
	browser.find_element_by_id("btnName").click()
	try:
		k = 1
		while k < 10:
			for j in range(0,9):
				try:			
					browser.find_element_by_id("DGalarmco").find_elements_by_tag_name("input")[j].click()
					info = []
					info.append("Licensed Alarm Company")
					try:
						alert = browser.switch_to_alert()
						print alert.text
						info.append(alert.text)
						alert.dismiss()
					except:
						info.append("")
					soup = BeautifulSoup(browser.page_source)
					info.append(soup.findAll("span",{"id":"lblLicNumber"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"lblLicExpData"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"lblRenewalDate"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"LblAgency"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"LblAgncyStreet"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"LblAgncyCity"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"LblAgncyState"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"LblAgncyZip"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"LblAgncyTelephone"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"LblDBAdata"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"lblFirst"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"lblMiddle"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"lblLast"})[0].text.strip())
					info.append(soup.findAll("span",{"id":"LblStatusData"})[0].text.strip())
					info[12] = (info[12] + " " + info[13] + " " + info[14])
					info.append("1")
					f.write("\"" + "\",\"".join(info) + "\"\n")
					print "\"" + "\",\"".join(info) + "\"\n"
					browser.find_element_by_id("btnPrev").click()
					#browser.back()
				except Exception, e:
					print str(e)
			k = k + 1
			try:
				browser.find_element_by_link_text("%s"%k).click()
			except:
				browser.find_element_by_xpath("//*[@id='btnNewSearch']").click()
	except Exception, e:
		print str(e)



f.close()
browser.close()
browser.quit()


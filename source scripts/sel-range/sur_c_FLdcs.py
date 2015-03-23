import sys, re, requests, codecs, csv
from bs4 import BeautifulSoup
from glob import glob
from selenium import webdriver
from datetime import date

year = date.today().year
month = date.today().month
day = date.today().day


f = codecs.open('sur_c_FLdcs_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')
t = codecs.open('sur_c_FLdcs.txt', 'w', 'utf-8')

#need path
browser = webdriver.PhantomJS()
browser.get("https://csapp.800helpfla.com/cspublicapp/businesssearch/businesssearch.aspx")
browser.find_element_by_css_selector("option[value=LB]").click()
browser.find_element_by_css_selector("input[value='Search']").click()
browser.find_element_by_css_selector("option[value=ALL]").click()
soup = BeautifulSoup(browser.page_source)
t.write(browser.page_source)

f.write("dba,company_name,company_address1,phone,licensee_type_cd,license_number,first_issue_date,expiration_date,status,license_type2,license2,issue_date2,expiration_date2,status2,license_type3,license3,issue_date3,expiration_date3,status3,license_type4,license4,issue_date4,expiration_date4,status4,license_type5,license5,issue_date5,expiration_date5,status5,company_flag,number_type,\n")

i = 0
while i < 1408:
	
	table1 = soup.find("table", id="cpMainContent_MasterGv_main_%d"%i)
	tablei = table1.find_all("table")[0]
	tableii = table1.find_all("table")[2]

	data = []
	tr = table1.find_all("td")[-1].text
	if "DBA/Other Names" in tr:
		tr = tr.replace ("DBA/Other Names", "")
		data.append(tr.strip())
	else:
		data.append(" ")
	for td in tablei.find_all("td"):
		data.append(td.text.strip())
	for bold in tableii.find_all("strong"):
		bold.decompose()
	for td in tableii.find_all("td"):
		data.append(td.text)

	data = "\",\"".join(data).replace("Phone", "\",\"")
	data = data.split("\",\"")

	try:
		del(data[4])
		del(data[4])
		del(data[4])
		del(data[4])
		del(data[4])		
	except:
		pass
	line =  '\"' + '\",\"'.join(data) + "\"\n"
	line = re.sub("\s\s*", " ", line)
	
	print(line + "\n")
	f.write(line + "\n")
	i = i+1

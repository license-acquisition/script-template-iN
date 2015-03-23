#******************************
# Web Scrape of IL Pest Control
# Site: http://ehlicv5pub.illinois.gov/Clients/ILDOHENV/PUBLIC/Pest_BusinessVerification.aspx

# Anthony Nault
# 08/15/2014
#******************************
import sys, csv, re, requests, time, string, codecs 
from bs4 import BeautifulSoup
from selenium import webdriver # Automate browser.
from selenium.webdriver.common.by import By # For waiting for page loads.
from selenium.webdriver.support.ui import WebDriverWait # For waiting for page loads.
from selenium.webdriver.support import expected_conditions as EC # Wait for load.
from datetime import date

start = time.time()

f = codecs.open('pes_c_ILdph_%s_000.csv' % (time.strftime('%Y%m%d')), 'w', 'UTF-8') 

#---------------------------- Define Headers for the Data --------------------------------
headers = ["entity_name", "license_number", "expiration_date", "Employee CCH", "certification1", "certification2", "certification3", "company_name", "Business License ID", "address1", "city", "state", "zip", "phone", "number_type", "licensee_type_cd", "company_flag", "county_flag", "city_flag"]

f.write("\"" + "\",\"".join(headers) + "\"\n")

i = 0
largeGap = 1000
gap = 0
while True:

	try:
		
		i += 1
		gap += 1
		if gap > largeGap * 2 and i >1500000:
			break

		if i == 10000:
			# There is a large Gap in the URL index for where we can find data.
			i = 1300000
 
		url = 'http://ehlicv5pub.illinois.gov/Clients/ILDOHENV/PUBLIC/PEST_BUSINESS_DETAILS.ASPX?ENTITYID=%d' % i

		page = requests.get(url)
		soup = BeautifulSoup(page.content.replace('<BR />', '|'))

		info = []

		business_name = soup.find('span', id = 'lblBusName').text
		business_license = soup.find('span', id = 'lblBusFileNum').text
		address = soup.find('span', id = 'lblBusAddr').text.split('|')
		street = address[0] # street
		city_state_zip = address[1].split(',')
		city = city_state_zip[0]
		state_zip = city_state_zip[1].split()
		state = state_zip[0] # state
		zipcode = state_zip[1] # zip
		phone = address[2] # phone

		employees = soup.find('table', id = 'dtgList').find_all('tr')[1:-2]
		for employee in employees:
			for td in employee.find_all('td'):
				info.append(td.text) # Employee Name to Certification Categories.
			info.append(business_name)
			info.append(business_license)
			info.append(street)
			info.append(city)
			info.append(state)
			info.append(zipcode)
			info.append(phone)
			info.append("Employee License ID")
			info.append("Pest Control")
			certifications = info[4].split(',')
			while len(certifications) < 3:
				certifications.append("")
			certification1 = certifications[0]
			certification2 = certifications[1]
			certification3 = certifications[2]
			info[4:5] = certification1, certification2, certification3
			f.write("\"" + "\",\"".join(info) + "\"\n")
			print "\"" + "\",\"".join(info) + "\"\n"
			print "ULR index: %d" %i
			print '-' * 50
			info = []
		
		if gap > largeGap:
			largeGap = gap
		
		gap = 0
			
	except Exception as e:
		print str(e)
		print "You stare into the abyss and go insane. Good job!"
		print "Invalid URL index: %d" % i
		print '-' * 50

end = time.time()

dt = end - start

print '*************'
print "Run Time = %d seconds" % dt
print '*************'	

	




















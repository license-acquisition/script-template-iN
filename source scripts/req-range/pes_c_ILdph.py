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
from script_template import create_file, logger

f = create_file('pes_c_ILdph', 'w', ['12', '21', '13', 'Employee CCH', '57', '58', '59', '7', 'Business License ID', '0', '4', '36', '44', '33', '102', '32', '6', '9', '5'])
l = logger('pes_c_ILdph')

def main():
	i = 0
	while i < 1500000:
		try:
			i += 1

			if i == 10000: # There is a large Gap in the URL index for where we can find data.
				i = 1300000
	 
			url = 'http://ehlicv5pub.illinois.gov/Clients/ILDOHENV/PUBLIC/PEST_BUSINESS_DETAILS.ASPX?ENTITYID=%d' % i

			soup = BeautifulSoup(requests.get(url).content.replace('<BR />', '|'))

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
				for m in [business_name, business_license, street, city, state, zipcode, phone, 'Employee License ID', 'Pest Control']
					infol.append(m)
				certifications = info[4].split(',')
				while len(certifications) < 3:
					certifications.append("")
				certification1 = certifications[0]
				certification2 = certifications[1]
				certification3 = certifications[2]
				info[4:5] = certification1, certification2, certification3
				f.write("|".join(info) + "\n")
				l.info(info)
				print "ULR index: %d" %i
				info = []
		except Exception as e:
			l.error('Error on %s: %s' %i, str(e))
			# print "You stare into the abyss and go insane. Good job!"


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()


















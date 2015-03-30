#*****************************
# Web Scrape of Oregon Landscape Contractors
# Site: http://www.oregonlcb.com/contractorsearch/ContractorSearch.aspx?styp=1

# Anthony Nault
# 8/18/2014
#*****************************

import csv, re, requests, time, string, codecs 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
from script_template import create_file, logger

f = create_file('lan_b_ORlcb', 'w', ['12', '6', '21', '102', 'DBA', '37', '0', '4', '36', '44', '13', '33', '32', '8', 'Backflow Status', '60', '19', 'Employer License Number', '65', 'Employer Relationship Status', '45', '71', 'Employee License Number', 'Emploeyee Name', 'Employee Relationship Status'])
l = logger('lan_b_ORlcb')
driver = webdriver.PhantomJS()

def main():
	info = [] # Lots of cool things will get put in here.
	# Search for business name that contains the given vowel (to give an exhaustive search.) Note: these results will not be mutally exclusive, so we will need to dedupe in the end.
	vowels = ['a', 'e', 'i', 'o', 'u']
	for vowel in vowels:
		url = 'http://www.oregonlcb.com/contractorsearch/ContractorSearch.aspx?styp=1'
		driver.get(url) # Opens the url in driver

		# Locate page elements
		enter_name = driver.find_element_by_id('MainContent_txtGeneralSearch')
		enter_name.send_keys(vowel)
		search = driver.find_element_by_id('MainContent_btnSimpleSearch')
		search.click()

		soup = BeautifulSoup(driver.page_source)

		results = soup.find('table', id = 'MainContent_gvResults')
		details = results.find_all('a')
		for detail in details:
			try:
				# Try to parse detail record.
				partial_link = detail['href']
				url = 'http://www.oregonlcb.com/contractorsearch/' + partial_link
				page = requests.get(url)
				soup = BeautifulSoup(page.content.replace('<br>', "|"))

				info = []

				# Get license info for business.
				business_details = soup.find('table', id = 'MainContent_tblBusinessDetails')
				for tr in business_details.find_all('tr'):
					tds = tr.find_all('td')
					for td in tds:
						if ':' in td.text:
							info.append(tds[tds.index(td) + 1].text)
				try:
					# Try to find employees.
					employee_table = soup.find('table', id = 'MainContent_grdEmployees')
					for tr in employee_table.find_all('tr')[1:]:
						for td in tr.find_all('td'):
							info.append(td.text)
				except Exception, e:
					# No employees found.
					l.debug("No employees found")
					l.debug(str(e))
					l.debug('-' * 25)
				
				info.insert(1, '1') # company_flag
				info.insert(3, "License Number") # number_type

				# Make adjustments to preserve alignment.
				info.insert(14, "")
				info.insert(15, "")
				info.insert(16, "")

				# Parse Address
				address = info[6].split('|')
				address1 = address[0]
				city_state_zip = address[1].split(',')
				city = city_state_zip[0]
				state_zip = city_state_zip[1].split()
				state = state_zip[0]
				zip_cd = state_zip[1]
				
				info[6:7] = address1, city, state, zip_cd

				f.write("|".join(info) + "\n")
				l.info(info)
				info = []

				# We have parsed the comapny license info. Move on to employees.

				try:
					# Get individual license info.
					employees = employee_table.find_all('a')
					for employee in employees:
						partial_link = employee['href']
						url = 'http://www.oregonlcb.com/contractorsearch/' + partial_link
						page = requests.get(url)
						soup = BeautifulSoup(page.content.replace('<br>', '|'))

						individual_details = soup.find('table' , id = 'MainContent_tblIndividualDetails')
						for tr in individual_details.find_all('tr'):
							tds = tr.find_all('td')
							for td in tds:
								if ':' in td.text:
									info.append(tds[tds.index(td) + 1].text)
						try:
							employment_history = soup.find('table', id = 'MainContent_grdEmploymentHistory')
							for tr in employment_history.find_all('tr')[1:2]:
								for td in tr.find_all('td'):
									info.append(td.text)
						except Exception as e:
							# No employee history found.
							l.error("No employee history found.")
							l.error(str(e))

						info.insert(1, "") # company_flag
						info.insert(3, "License Number") # number_type

						# Make sure data falls in the right headers.
						info.insert(6, info[4])
						info[4] = ""
						info[7], info[8] = info[8], info[7]
						info[9], info[10] = info[10], info[9]
						info.insert(12, "") # company_type

						# Parse Address
						address = info[6].split('|')
						address1 = address[0]
						city_state_zip = address[1].split(',')
						city = city_state_zip[0]
						state_zip = city_state_zip[1].split()
						state = state_zip[0]
						zip_cd = state_zip[1]
						info[6:7] = address1, city, state, zip_cd

						f.write("|".join(info) + "\n")
						l.info(info)
						info = []		

				except Exception as e:
					# No individual licensee found.
					l.error("No individual found.")
					l.error(str(e))
					l.error('-' * 25)
			except Exception as e:
				# No detail record found.
				l.error("Ooops, detail record missing. Continue...")
				l.error(str(e))
				l.error('-' * 25)


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: 
        f.close()
        driver.quit()
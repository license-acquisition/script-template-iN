#************************************************************************
# New Jersey Department of Environmental Protection Pest Control Web Scrape
# Site: http://datamine2.state.nj.us/DEP_OPRA/OpraMain/categories?category=Pesticides

# Anthony Nault
# 07/16/2014
#********************* Using Selenium with Beautiful Soup ************

# This script has two main parts. First we aquire company licnese info. This dataset will give us individual licensee names. The second half of this script will take those names and use them to query the a different database of individual licensees. (FYI this was a clever work around for needing an exact individual name.) In the end, all the data will get combinded into a single feed.
'''
Download the HTML pages 
1. navigate to: http://datamine2.state.nj.us/DEP_OPRA/OpraMain/categories?category=Pesticides
2. click: Applicator businesses by types of pest control Performed
3. click: 'All' counties
4. select three types of work performed
5. right click, save page as NJ_pes_(number of page)
6. repeat until all types of work have been selected and saved.
'''
import time, re, csv, codecs, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import pandas # For general data analysis. Also, read functionality for CSVs.
from script_template import create_file, logger

f = create_file("pes_b_NJdep","w",[32,21,12,6,"Responsible_Applicator",0,"city and state",8,33,37,13,"employer"])




# Instantiate CSV file
#g = codecs.open('Responsible_Applicator.csv', 'w', 'UTF-8') # Secondary File


# Define Headers for the data.

# Instantiate Webdriver.
#browser = webdriver.Chrome()

#========================== PART ONE: Company License Acquisition ===========================

# get the local document.
#url = 'http://datamine2.state.nj.us/DEP_OPRA/OpraMain/categories?category=Pesticides'
def main():
	for j in range(1,9):
		local_doc = "C:\Users\Chris Jimenez\Desktop\NJ_pes\NJ_pes_%d.html" % j
		web_page = open(local_doc).read()






		# Parse HTM
		#soup = BeautifulSoup(browser.page_source)
		soup = BeautifulSoup(web_page)
		data = soup.find('div', {'id':"display"}) #This section has the table we want.
		tables = data.find_all('table', {'width':"639"}) # This is a list of all table records.

		# Loop through each table on the page, parse HTML and write to CSV.  
		for table in tables:

			try:

				info = [] # A holding tank for data

				# In each table loop through a select range of rows.
				for tr in table.find('table').find_all('tr')[1:23:3]:
					# Get licensee basic information.
					td = tr.find_all('td')[1]
					info.append(re.sub('.*:','',''.join(c for c in td.text if 0 < ord(c) < 127)))
				# Get licensee status and exp. date.
				info.append(''.join(c for c in table.find('table').find_all('tr')[28].find_all('td')[0].text if 0 < ord(c) < 127))
				info.append(''.join(c for c in table.find('table').find_all('tr')[28].find_all('td')[2].text if 0 < ord(c) < 127))
				
				info.insert(3, '1') # company_flag

				f.write("\"" + "\"|\"".join(info) + "\"\n") # Write to Main CSV
				#g.write("\"" + "\"|\"".join(info) + "\"\n") # Wrtie to secondary file.
			

			except Exception as e:
				l.error(str(e))
		
		
		soup.decompose()
	#g.close()
if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		l.critical(str(e))
	finally:
		f.close()
#======================== PART TWO: Individual License Acquisition ==========================
'''

#ind_headers = ["License Number", "Name", "License Type", "Employer", " Employer Address", "Employer City, State", "Employer County", "Employer Phone", "Status", "Expiration Date"]


info = []

# Get individual licensee names from CSV.
data = pandas.read_csv('Responsible_Applicator.csv', names = headers)
names = list(data.Responsible_Applicator) # Store individual licensee names in a list.

# Make lists of first names and last names.
first_names = []
last_names = []

for name in names[1:]:
	first_names.append(name.split(" ")[0])
	last_names.append(name.split(" ")[1])

# Search every name given by our list of first names and last names:
for i in range(0, len(last_names) - 1):

	try:

		# Navigate to the Individual Commercial Applicator search portal.
		url = "http://datamine2.state.nj.us/DEP_OPRA/OpraMain/categories?category=Pesticides"
		browser.get(url)
		applicators_by_name = browser.find_element_by_link_text("Commercial Certified Pesticide Applicators by Name")
		applicators_by_name.click()

		# Wait for search field to appear on page.
		try:
			last = WebDriverWait(browser, 1800).until(
					EC.presence_of_element_located((By.XPATH, "//*[@id=\"display\"]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/input"))
				)
		except Exception as e:
			# Page took too long to load.
			print "WHERE ARE MY DRAGONS?!"
			print str(e)
	
		# Identify search fields on page.
		search_last = browser.find_element_by_xpath("//*[@id=\"display\"]/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/input")
		search_first = browser.find_element_by_xpath("//*[@id=\"display\"]/table/tbody/tr[3]/td/table/tbody/tr[3]/td[2]/input")

		# from fist and last name lists, enter search criteria.
		search_last.send_keys(last_names[i])
		search_first.send_keys(first_names[i])

		# Execute search.
		ok = browser.find_element_by_xpath("//*[@id=\"display\"]/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/input[2]")
		ok.click()

		# Wait for table data to appear.
		try:
			table = WebDriverWait(browser, 1800).until(
					EC.presence_of_element_located((By.XPATH, "//*[@id=\"display\"]/table[4]/tbody/tr/td[2]/table"))
				)
		except Exception as e:
			# Data took too long to load
			print "WHERE ARE MY DRAGONS?!"
			print str(e)

		#Parse detail record.
		soup = BeautifulSoup(browser.page_source)
		tds = soup.find_all('td')

		info.append(''.join(c for c in tds[77].text if 0 < ord(c) < 127)) # License Type
		info.append(re.sub(".*:","",''.join(c for c in tds[55].text if 0 < ord(c) < 127))) # Lic Number
		info.append(''.join(c for c in tds[76].text if 0 < ord(c) < 127)) # Licensee Name
		info.append("") # company_flag
		info.append("") # Responsible_Applicator
		
		info.append(''.join(c for c in tds[103].text if 0 < ord(c) < 127)) # Employer Address
		info.append(''.join(c for c in tds[104].text if 0 < ord(c) < 127)) # Employer City/State
		info.append(''.join(c for c in tds[105].text if 0 < ord(c) < 127)) # Employer County
		info.append(''.join(c for c in tds[106].text if 0 < ord(c) < 127)) # Employer Phone

		for td in tds:
			if td.text == "Current Status":
				info.append(tds[tds.index(td) + 1].text) # Current Status
			if td.text == "For License Period Expiring:":
				info.append(tds[tds.index(td) + 1].text) # Expiration Date

		info.append(''.join(c for c in tds[102].text if 0 < ord(c) < 127)) # Employer Name

		if len(info) > 12:
			# The parsing did not come out right.
			info[11] = info[-1] # Make sure employer name falls on the correct index.
			while len(info) > 12:
				del info[-1] # Cuts off result of bad parsing.

		f.write("\"" + "\",\"".join(info) + "\"\n") # Write to CSV
		print "\"" + "\",\"".join(info) + "\"\n" # Print row for sanity check.
		print "Record # %d out of %d" % (i + 1, len(last_names)) 
		print '-' * 50
		info = []
		
	except Exception as e:
		print "Parse fail. Next record..."
		print str(e)
		print '-' * 25
		continue


#f.close()'''

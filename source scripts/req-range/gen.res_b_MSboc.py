#**********************************************************************************
# Web Scrape of Mississippi Board of Contractors
# Site: http://www.msboc.us/ConsolidatedResults.CFM?ContractorType=&VarDatasource=BOC

# Anthony Nault
# 08/01/2014
#************************* Using Requests with Beautiful Soup *********************
import csv, re, requests, time, string, codecs
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('gen.res_b_MSboc', 'w', ['12', '6', '9', '5', '102', '21', '32', '0', '4', '36', '8', '44', '33', '66', 'DBA', '13', 'Minority', '57', '35', '58', 'qualifying_individual2', '59', 'qualifying_individual3', 'certification4', 'qualifying_individual4', 'certification5', 'qualifying_individual5', 'Officer 1 Name', 'Officer 1 Title', 'Officer 2 Name', 'Officer 2 Title', 'Officer 3 Name', 'Officer 3 Title', 'Officer 4 Name', 'Officer 4 Title', '62', 'Complaint Date 1', '63', 'Resoultion Date 1', 'Complaint 2', 'Complaint Date 2', 'Resolution 2', 'Resoultion Date 2Complaint 3', 'Complaint Date 3', 'Resolution 3', 'Resoultion Date 3'])
l = logger('gen.res_b_MSboc')

#---------------------------- Define Parsing Function -----------------------------

def parse(soup):
	#Parses the record's source HTML and writes a row of data to our CSV
	
	info = [] # Lots of cool stuff will be put in here.

	# Get basic license data.
	trs = soup.find_all('tr')
	for tr in trs:
		# Get basic license info.
		if "Class(es)" in tr.text:
			class_index = trs.index(tr) # The start of classification data.
			break
		tds = tr.find_all('td')
		if trs.index(tr) == 0:
			info.append(tds[0].text)
			continue
		info.append(tds[1].text)
		if "State" in tds[0].text and "MS" not in tds[1].text:
			info.append("") # Compensation for missing county

	# See if Class(es) table is populated.
	if "(None)" not in trs[class_index + 1]:
		class_index += 4
	else:
		class_index += 1

	# Get classification info.			
	for tr in trs[class_index: -1]:
		if "Officers" in tr.text:
			officer_index = trs.index(tr) # The start of officer data.
			break
		for td in tr.find_all('td'):
			if "(None)" in td.text:
				break
			info.append(td.text)

	while len(info) < 22:
		info.append("") # Compensate for missing class(es)
	while len(info) > 22:
		del(info[-1]) # Trim excess classifications

	# See if Officers table is populated.
	if "(None)" not in trs[officer_index + 1].text:
		officer_index += 4
	else:
		officer_index += 1
	
	# Get officer info.			
	for tr in trs[officer_index: -1]:
		if "Violations" in tr.text:
			violation_index = trs.index(tr) + 4 # The start of violation data.
			break
		for td in tr.find_all('td'):
			if "(None)" in td.text:
				break
			info.append(td.text)

	while len(info) < 30:
		info.append("") # Compensate for missing officer(s)
	while len(info) > 30:
		del(info[-1]) # Compensate for excess officer(s).

	try:
		# Try to find violation info.
		for tr in trs[violation_index: -1]:
			for td in tr.find_all('td'):
				info.append(td.text)
	except:
		pass # I assume no violation information was found.


	while len(info) < 36:
		info.append("") # Compensate for missing violations.
	while len(info) > 36:
		del(info[-1]) # Compensate for excess violations.

	if " &" in info[0] or " INC" in info[0] or " LLC" in info[0] or " CO." in info[0]:
		# Add a company flag to the record
		info.insert(1, '1')
	else:
		info.append(1, "")

	info.insert(2, "") # county_flag
	info.insert(3, "") # city_flag
	info.insert(4, "License Number") # number_type

	if "Commercial" in url:
		info.insert(6, "Commercial Contractor") # licensee_type_cd
	else:
		info.insert(6, "Residential Contractor") # licensee_type_cd

	f.write("|".join(info) + "\n")
	l.info(info)
	l.info('-' * 50)


#-------------------------------------- Parse HTML --------------------------------
def main():	
	largeGap = 1000
	gap = 0
	i = 7000 # originally 7000
	while True:
		try:
			# Try to find a valid URL and get data.
			i += 1
			gap += 1

			if gap > largeGap * 2 and i > 50000:
				break
			if i <= 30000:	
				url = "http://www.msboc.us/Detail.cfm?ContractorID=%d&ContractorType=Commercial&varDataSource=BOC" % i
			elif i > 30000:
				url = "http://www.msboc.us/Detail.cfm?ContractorID=%d&ContractorType=Residential&varDataSource=BOCRes" % i
			
			soup = BeautifulSoup(requests.get(url).content)

			parse(soup)

			if gap > largeGap:
				largeGap = gap
			gap = 0

		except Exception as e:
			# I assume that the url leads to a blank page.
			l.debug("Oops, invalid URL index: %d. Try again..." % i)
			l.debug('-' * 25)

		
if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception as e: l.critical(str(e))
	finally: f.close()
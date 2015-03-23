#********************
# Washington Labor and Industry Asbestos Certification Scrape
# Anthony Nault
# 7/10/2014
#********************

import csv, re, requests, time
from bs4 import BeautifulSoup

#********************* Name the File You Want to Put Your Data Into **********************

f = open('asb_c_WAdli_%s_000.csv'%(time.strftime("%Y%m%d")),'w')

#**************************** Define Headers for the Data ********************************

headers = ["entity_name", "address1", "address2", "email", "qualifying_individual", "phone", "fax", "license_number", "expiration_date"]

f.write("|".join(headers) + "\n")
 
#******************************* Get URL to Scrape ***************************************

url = "http://www.lni.wa.gov/Safety/Topics/AtoZ/Asbestos/contractorlist.asp"
page = requests.get(url)
soup = BeautifulSoup(page.content.replace('<br />', '|'))

#********************************* Parse HTML ********************************************


trs = soup.find_all('tr')[2:]

for tr in trs:
	
	info = []
	
	for td in tr.find_all('td'):
		
		rows = td.text.split('|')
		l = len(rows)
		
		# Modify length of rows to preserve alignment in the CSV
		if tr.find_all('td').index(td) == 0:	
			if l < 4:
				while l < 4:	
					rows.append("")
					l = len(rows)							
		if tr.find_all('td').index(td) == 1:	
			if l < 3:
				while l < 3:	
					rows.append("")
					l = len(rows)			
		if tr.find_all('td').index(td) == 2:
			if l < 2:
				while l < 2:
					rows.append("")
					l = len(rows)
				
		for data in rows:
			
			data = re.sub('\xa0',"",data)
			data = re.sub('\s\s*'," ",data)
			
			info.append(data)		
	
	f.write("|".join(info) + "\n")	
	# print "\"" + "\",\"".join(info) + "\"\n"

f.close()
		



		







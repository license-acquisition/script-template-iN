#*****************************************************************************************
# Miami Dade, Florida Contractor Web Scrape.
# Site: http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAWBCC.DIA

# Anthony Nault
# 07/11/2014
#*****************************************************************************************

import csv, re, requests, time, codecs
from bs4 import BeautifulSoup
from datetime import date


start=time.time()

start = time.time() # We are going to keep track of how long the program runs.

#********************* Name the File You Want to Put Your Data Into **********************

f = codecs.open('gen.res_b_FL.MDbui_%s_000.csv' %(time.strftime('%Y%m%d')), 'w', 'utf-8')

#**************************** Define Headers for the Data ********************************




headers = ["license_number", "entity_name", "address1", "city", "state", "zip", "phone", "phone2", "fax", "email", "dba", "status", "Class_1", "Category_1", "Category_Description_1", "expiration_date", "Class_2", "Category_2", "Category_Description_2", "expiration_date2", "Class_3", "Category_3", "Category_Description_3", "expiration_date3", "Class_4", "Category_4", "Category_Description_4", "expiration_date4", "Class_5", "Category_5", "Category_Description_5", "expiration_date5","number_type","licensee_type_cd","company_flag"]

f.write("|".join(headers) + "\n")

#*************************** Define Parsing Function *************************************

search_fail = 0 # This is a variable we will use to track whether or not we were successful at finding a record.

# A function that will parse the HTML on the current page and write a row to our CSV
def parse():	
	try:
		tables = soup.find_all('table')
		info = []
		# Get Contractor License Information
		for tr in tables[5].find_all('tr'):
			for td in tr.find_all('td')[1:]:
				info.append(re.sub("\s\s*"," ",''.join(c for c in td.text if 0 < ord(c) < 127)))
		# Get Category Description	
		for tr in tables[6].find_all('tr')[1:]:
			for td in tr.find_all('td'):
				info.append(re.sub("\s\s*"," ",''.join(c for c in td.text if 0 < ord(c) < 127)))
		# Write new row to CSV	
		f.write("\"" + "\",\"".join(info) + "\"\n")		
		print "\"" + "\",\"".join(info) + "\"\n" 
		return True # URL index successfully corresponded to a valid record. 			
	except Exception as e:
		print str(e)
		return False # URL index did not correspond to a valid record.
		
# There are a lot of URLs to loop through, we dont want to have to check them all. So we keep track of the number of failed attempts in a row. We stop checking when the number of consecutive failed attempts becomes really large.		
	
#******************************* Get URL to Scrape ***************************************

# This authority is a real pain. There are basically 5 different formats that the URL can come in (that I narrowed down to the best of my ability). 1. 0000XXXXX 2. XXB0XXXXX 3. XXP0XXXXX 4. XXE0XXXXX 5. XXBSXXXXX. We need five major loops to check all these variations, and - hold on to your pants - loops within loops!

fail_1 = [] # We are going to keep track of our consecutive fails

# Index format 0000XXXXX
for i in range(0, 20000):

	# Keep track of the total number of consecutive fails.
	if search_fail == 1000:
		print "TERMINUS"
		print '-' * 50
		search_fail = 0 # Reset so we start fresh for the next loop.	
		break # We failed 1000 times in a row. Time to move on!
				
	if i < 10:
		url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=00000000%d"   % i 
	elif i < 100:
		url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0000000%d"  % i
	elif i < 1000:
		url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=000000%d"  % i
	elif i < 10000:
		url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=00000%d" %  i
	elif i < 100000:
		url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0000%d" % i

	page = requests.get(url)
	soup = BeautifulSoup(page.content)

#********************************* Parse HTML ********************************************
	
	# Executes parse(). If parse() returns true then we have a record, else we fail.
	if parse():
		fail_1.append(search_fail) # Store the previous number of consecutive fails.
		search_fail = 0 # We found a record! Reset.
		print "All your tds are belong to us!"
		print '-' * 50
	else:
		search_fail += 1 # We did not find a record
		print "Consecutive Search Fail #: %s; i = %s" % (search_fail, i)
		print '-' * 50
		continue # In parse() our try failed, but we want to iterate again.		
	
# End for. We have concluded Method 1.

print "End of 0000XXXXX search."
print "Largest streak of consecutive fails = %d." % max(fail_1)
print '*' * 70
print
#******************************* Get URL to Scrape ***************************************

fail_2 = [] # We are going to keep track of our consecutive fails
		
# Index format XXB0XXXXX
for i in range(0, 100):
	for j in range(0, 20000):
		
		# Keep track of the total number of consecutive fails.
		if search_fail == 1000:
			print "TERMINUS"
			print '-' * 50
			search_fail = 0	# Reset so we start fresh for the next loop.
			break # We failed 1000 times in a row. Time to move on!
		
		if i < 10:
		
			if j < 10:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB00000%d" % (i,j)
			elif j < 100:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB0000%d" % (i,j)
			elif j < 1000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB000%d" % (i,j)
			elif j < 10000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB00%d" % (i,j)
			elif j < 100000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB0%d" % (i,j)
				
				
		elif i < 100:
		
			if j < 10:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB00000%d" % (i,j)
			elif j < 100:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB0000%d" % (i,j)
			elif j < 1000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB000%d" % (i,j)
			elif j < 10000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB00%d" % (i,j)
			elif j < 100000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dB0%d" % (i,j)
			
		page = requests.get(url)
		soup = BeautifulSoup(page.content)
	
#********************************* Parse HTML ********************************************

		# Executes parse(). If parse() returns true then we have a record, else we fail.
		if parse():
			fail_2.append(search_fail) # Store the previous number of consecutive fails.
			search_fail = 0 # We found a record!
			print "All your tds are belong to us!"
			print '-' * 50
		else:
			search_fail += 1 # We did not find a record
			print "Consecutive Search Fail #: %s; i = %s, j = %s" % (search_fail, i, j)
			print '-' * 50
			continue # In parse() our try failed, but we want to iterate again.
				
# End for. We have concluded Method 2.

print "End of XXB0XXXXX search."
print "Largest streak of consecutive fails = %d." % max(fail_2)
print '*' * 70
print
#******************************* Get URL to Scrape ***************************************	

fail_3 = [] # We are going to keep track of our consecutive fails
		
# Index format XXE0XXXXX
for i in range(0, 100):
	for j in range(0, 20000):
	
		# Keep track of the total number of consecutive fails.
		if search_fail == 1000:
			print "TERMINUS"
			print '-' * 50
			search_fail = 0 # Reset so we start fresh for the next loop.	
			break # We failed 1000 times in a row. Time to move on!
	
		if i < 10:
		
			if j < 10:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE00000%d" % (i,j)
			elif j < 100:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE0000%d" % (i,j)
			elif j < 1000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE000%d" % (i,j)
			elif j < 10000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE00%d" % (i,j)
			elif j < 100000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE0%d" % (i,j)
				
	
		elif i < 100:
		
			if j < 10:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE00000%d" % (i,j)
			elif j < 100:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE0000%d" % (i,j)
			elif j < 1000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE000%d" % (i,j)
			elif j < 10000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE00%d" % (i,j)
			elif j < 100000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dE0%d" % (i,j)
			
		page = requests.get(url)
		soup = BeautifulSoup(page.content)

#********************************* Parse HTML ********************************************

		# Executes parse(). If parse() returns true then we have a record, else we fail.
		if parse():
			fail_3.append(search_fail) # Store the previous number of consecutive fails.
			search_fail = 0 # We found a record!
			print "All your tds are belong to us!"
			print '-' * 50
		else:
			search_fail += 1 # We did not find a record
			print "Consecutive Search Fail #: %s; i = %s, j = %s" % (search_fail, i, j)
			print '-' * 50
			continue # In parse() our try failed, but we want to iterate again.
				
# End for. We have concluded Method 3.

print "End of XXE0XXXXX search."
print "Largest streak of consecutive fails = %d." % max(fail_3)
print '*' * 70
print
#******************************* Get URL to Scrape ***************************************

fail_4 = [] # We are going to keep track of our consecutive fails

# Index format XXP0XXXXX
for i in range(0, 100):
	for j in range(0,20000):
	
		# Keep track of the total number of consecutive fails.
		if search_fail == 1000:
			print "TERMINUS"
			print '-' * 50
			search_fail = 0	# Reset so we start fresh for the next loop.
			break # We failed 1000 times in a row. Time to move on! """
	
		if i < 10:
		
			if j < 10:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP00000%d" % (i,j)
			elif j < 100:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP0000%d" % (i,j)
			elif j < 1000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP000%d" % (i,j)
			elif j < 10000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP00%d" % (i,j)
			elif j < 100000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP0%d" % (i,j)
				
	
		elif i < 100:
		
			if j < 10:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP00000%d" % (i,j)
			elif j < 100:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP0000%d" % (i,j)
			elif j < 1000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP000%d" % (i,j)
			elif j < 10000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP00%d" % (i,j)
			elif j < 100000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dP0%d" % (i,j)
			
		page = requests.get(url)
		soup = BeautifulSoup(page.content)

#********************************* Parse HTML ********************************************

		# Executes parse(). If parse() returns true then we have a record, else we fail.
		if parse():
			fail_4.append(search_fail) # Store the previous number of consecutive fails.
			search_fail = 0 # We found a record!
			print "All your tds are belong to us!"
			print '-' * 50
		else:
			search_fail += 1 # We did not find a record
			print "Consecutive Search Fail #: %s; i = %s, j = %s" % (search_fail, i, j)
			print '-' * 50
			continue # In parse() our try failed, but we want to iterate again.
				
# End for. We have concluded Method 4.

print "End of XXP0XXXXX search."
print "Largest streak of consecutive fails = %d." % max(fail_4)
print '*' * 70
print
#******************************* Get URL to Scrape ***************************************

fail_5 = [] # We are going to keep track of our consecutive fails

# Index format XXBSXXXXX
for i in range(0, 100):
	for j in range(0, 20000):
	
		# Keep track of the total number of consecutive fails.
		if search_fail == 1000:
			print "TERMINUS"
			search_fail = 0 # Reset so we start fresh on the next loop.	
			break # We failed 1000 times in a row. Time to move on!"""
	
		if i < 10:
		
			if j < 10:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS0000%d" % (i,j)
			elif j < 100:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS000%d" % (i,j)
			elif j < 1000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS00%d" % (i,j)
			elif j < 10000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS0%d" % (i,j)
			elif j < 100000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS%d" % (i,j)
				
	
		elif i < 100:
		
			if j < 10:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS0000%d" % (i,j)
			elif j < 100:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS000%d" % (i,j)
			elif j < 1000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS00%d" % (i,j)
			elif j < 10000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS0%d" % (i,j)
			elif j < 100000:
				url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=0%dBS%d" % (i,j)
			
		page = requests.get(url)
		soup = BeautifulSoup(page.content)

#********************************* Parse HTML ********************************************

		# Executes parse(). If parse() returns true then we have a record, else we fail.	
		if parse():
			fail_5.append(search_fail) # Store the previous number of consecutive fails.
			search_fail = 0 # We found a record!
			print "All your tds are belong to us!"
			print '-' * 50
		else:
			search_fail += 1 # We did not find a record
			print "Consecutive Search Fail #: %s; i = %s, j = %s" % (search_fail, i, j)
			print '-' * 50
			continue # In parse() our try failed, but we want to iterate again.
				
# End for. We have concluded Method 5.


print "End of XXBSXXXXX search."
print "Largest streak of consecutive fails = %d." % max(fail_1)
print '*' * 70
print
#***************************** Closing Up Shop *******************************************

print "****** THE END ******"

f.close # Closes our CSV.

# Figure out how long the script took to run.
end = time.time()
run_sec = end - start # How many seconds since the program started.
run_hour = run_sec/3600	

print '*' * 50
print "Gadzooks! This program took %d hours to run!" % run_hour
print '*' * 50
		







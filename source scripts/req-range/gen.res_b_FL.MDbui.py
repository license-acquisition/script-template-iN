#*****************************************************************************************
# Miami Dade, Florida Contractor Web Scrape.
# Site: http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAWBCC.DIA

# Anthony Nault
# 07/11/2014
#*****************************************************************************************

import csv, re, requests, time, codecs
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('gen.res_b_FL.MDbui', 'w', ['21', '12', '0', '4', '36', '44', '33', 'phone2', '66', '11', '10', '37', 'Class_1', 'Category_1', 'Category_Description_1', '13', 'Class_2', 'Category_2', 'Category_Description_2', '14', 'Class_3', 'Category_3', 'Category_Description_3', '15', 'Class_4', 'Category_4', 'Category_Description_4', '16', 'Class_5', 'Category_5', 'Category_Description_5', '17', '102', '32', '6'])
l = logger('gen.res_b_FL.MDbui')

#*************************** Define Parsing Function *************************************

# A function that will parse the HTML on the current page and write a row to our CSV
def parse(soup):	
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
		f.write("|".join(info) + "\n")		
		l.info(info)
		return True # URL index successfully corresponded to a valid record. 			
	except Exception as e:
		l.error(str(e))
		return False # URL index did not correspond to a valid record.
		
# There are a lot of URLs to loop through, we dont want to have to check them all. So we keep track of the number of failed attempts in a row. We stop checking when the number of consecutive failed attempts becomes really large.		
	
#******************************* Get URL to Scrape ***************************************

def main():
	# This authority is a real pain. There are basically 5 different formats that the URL can come in (that I narrowed down to the best of my ability). 1. 0000XXXXX 2. XXB0XXXXX 3. XXP0XXXXX 4. XXE0XXXXX 5. XXBSXXXXX. We need five major loops to check all these variations, and - hold on to your pants - loops within loops!
	search_fail = 0 # This is a variable we will use to track whether or not we were successful at finding a record.

	fail_1 = [] # We are going to keep track of our consecutive fails

	# Index format 0000XXXXX
	for i in range(0, 20000):

		# Keep track of the total number of consecutive fails.
		if search_fail == 1000:
			l.debug("TERMINUS")
			l.debug('-' * 50)
			search_fail = 0 # Reset so we start fresh for the next loop.	
			break # We failed 1000 times in a row. Time to move on!
		
		url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=%09d" %i		
		soup = BeautifulSoup(requests.get(url).content)

	#********************************* Parse HTML ********************************************
		
		# Executes parse(). If parse() returns true then we have a record, else we fail.
		if parse(soup):
			fail_1.append(search_fail) # Store the previous number of consecutive fails.
			search_fail = 0 # We found a record! Reset.
			l.debug("All your tds are belong to us!")
			l.debug('-' * 50)
		else:
			search_fail += 1 # We did not find a record
			l.debug("Consecutive Search Fail #: %s; i = %s" % (search_fail, i))
			l.debug('-' * 50)
			continue # In parse() our try failed, but we want to iterate again.		
		
	# End for. We have concluded Method 1.

	l.info("End of 0000XXXXX search.")
	l.info("Largest streak of consecutive fails = %d." % max(fail_1))
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
			
			url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=%02dB%06d" %(i,j)
			soup = BeautifulSoup(requests.get(url).content)
		
	#********************************* Parse HTML ********************************************

			# Executes parse(). If parse() returns true then we have a record, else we fail.
			if parse(soup):
				fail_2.append(search_fail) # Store the previous number of consecutive fails.
				search_fail = 0 # We found a record!
				l.info("All your tds are belong to us!")
				l.info('-' * 50)
			else:
				search_fail += 1 # We did not find a record
				l.info("Consecutive Search Fail #: %s; i = %s, j = %s" % (search_fail, i, j))
				l.info('-' * 50)
				continue # In parse() our try failed, but we want to iterate again.
					
	# End for. We have concluded Method 2.

	l.info("End of XXB0XXXXX search.")
	l.info("Largest streak of consecutive fails = %d." % max(fail_2))
	l.info('*' * 70)
	#******************************* Get URL to Scrape ***************************************	

	fail_3 = [] # We are going to keep track of our consecutive fails
			
	# Index format XXE0XXXXX
	for i in range(0, 100):
		for j in range(0, 20000):
		
			# Keep track of the total number of consecutive fails.
			if search_fail == 1000:
				l.info("TERMINUS")
				l.info('-' * 50)
				search_fail = 0 # Reset so we start fresh for the next loop.	
				break # We failed 1000 times in a row. Time to move on!
			
			url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=%02dE%06d" %(i,j)
			soup = BeautifulSoup(requests.get(url).content)

	#********************************* Parse HTML ********************************************

			# Executes parse(). If parse() returns true then we have a record, else we fail.
			if parse(soup):
				fail_3.append(search_fail) # Store the previous number of consecutive fails.
				search_fail = 0 # We found a record!
				l.info("All your tds are belong to us!")
				l.info('-' * 50)
			else:
				search_fail += 1 # We did not find a record
				l.info("Consecutive Search Fail #: %s; i = %s, j = %s" % (search_fail, i, j))
				l.info('-' * 50)
				continue # In parse() our try failed, but we want to iterate again.
					
	# End for. We have concluded Method 3.

	l.info("End of XXE0XXXXX search.")
	l.info("Largest streak of consecutive fails = %d." % max(fail_3))
	l.info('*' * 70)
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
			
			url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=%02dP%06d" %(i,j)

			soup = BeautifulSoup(requests.get(url).content)

	#********************************* Parse HTML ********************************************

			# Executes parse(). If parse() returns true then we have a record, else we fail.
			if parse(soup):
				fail_4.append(search_fail) # Store the previous number of consecutive fails.
				search_fail = 0 # We found a record!
				l.debug("All your tds are belong to us!")
				l.debug('-' * 50)
			else:
				search_fail += 1 # We did not find a record
				l.debug("Consecutive Search Fail #: %s; i = %s, j = %s" % (search_fail, i, j))
				l.debug('-' * 50)
				continue # In parse() our try failed, but we want to iterate again.
					
	# End for. We have concluded Method 4.

	l.debug("End of XXP0XXXXX search.")
	l.debug("Largest streak of consecutive fails = %d." % max(fail_4))
	l.debug('*' * 70)
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
			
			url = "http://egvsys.miamidade.gov:1608/WWWSERV/ggvt/BNZAW941.DIA?CNTR=%02dBS%05d" % (i,j)
			soup = BeautifulSoup(requests.get(url).content)

	#********************************* Parse HTML ********************************************

			# Executes parse(). If parse() returns true then we have a record, else we fail.	
			if parse(soup):
				fail_5.append(search_fail) # Store the previous number of consecutive fails.
				search_fail = 0 # We found a record!
				l.debug("All your tds are belong to us!")
				l.debug('-' * 50)
			else:
				search_fail += 1 # We did not find a record
				l.debug("Consecutive Search Fail #: %s; i = %s, j = %s" % (search_fail, i, j))
				l.debug('-' * 50)
				continue # In parse() our try failed, but we want to iterate again.
					
	# End for. We have concluded Method 5.


	l.debug("End of XXBSXXXXX search.")
	l.debug("Largest streak of consecutive fails = %d." % max(fail_1))
	l.debug('*' * 70)
	#***************************** Closing Up Shop *******************************************

	l.debug("****** THE END ******")

	f.close # Closes our CSV.

	# Figure out how long the script took to run.
	end = time.time()
	run_sec = end - start # How many seconds since the program started.
	run_hour = run_sec/3600	

	l.debug('*' * 50)
	l.debug("Gadzooks! This program took %d hours to run!" % run_hour)
	l.debug('*' * 50)
		

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()






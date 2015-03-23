#******************* METHOD 1: Using Beautiful Soup and Requests ******************

import csv, re, requests, time, string, codecs # for CSV files, Regex, getting URLs, time data, string has useful features like the alphabet, codecs.open can "Open an encoded file using the given mode and return a wrapped version providing transparent encoding/decoding."
from bs4 import BeautifulSoup # for parsing HTML

#--------------------- Name the File You Want to Put Your Data Into ---------------

f = codecs.open('asb_b_MIcsc_%s_000.csv' % time.strftime("%Y%m%d"),'w', 'UTF-8')

#---------------------------- Define Headers for the Data -------------------------

headers = ["enity_name","address1", "city, state, zip", "phone", "licensee_type_cd", "license_number", "status","", "expiration_date"]
f.write("\"" + "\",\"".join(headers) + "\"\n") 

#------------------------------- Get URL to Scrape --------------------------------

largeGap = 1000
gap = 0
i = 0
while True:
	try:
		i += 1
		gap +=1
		if gap > largeGap * 2 and i > 10000:
			break

		url = 'http://www.dleg.state.mi.us/asbestos_program/dt_contractor.asp?id=%d' % i
		soup = BeautifulSoup(requests.get(url).content)

		# Parse
		tables = soup.find('div', align = 'center').find_all('table')

		info = []
		for tr in tables[0].find_all('tr')[1:]:
			info.append(tr.find_all('td')[2].text.replace(u'\xa0',u''))

		for td in tables[1].find_all('tr')[2].find_all('td'):
			info.append(td.text.strip().replace(u'\xa0',u''))

		f.write("\"" + "\",\"".join(info) + "\"\n")
		print "\"" + "\",\"".join(info) + "\"\n"
		print '-' * 50
		info = []

		if gap > largeGap:
			largeGap = gap
			
		gap = 0


	except Exception as e:
		print str(e)
		print "KHAN!!!!!!!!!!!!!!!!!"
		print '-' * 25

f.close()

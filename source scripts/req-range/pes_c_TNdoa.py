#********************
# Tennessee Department of Agriculture Pest Control Scrape
# @author Anthony Nault
# @contributor Chris Jimenez
# 07/09/2014
# edited 01/26/2015
#********************

import csv, re, requests, time
from bs4 import BeautifulSoup

f = open('pes_c_TNdoa_%s_000.csv'%time.strftime('%Y%m%d'),'w') 

headers = ["license_number", "entity_name", "address1", "address2", "city,state,zip", "phone", "first_issue_date", "last_renew_date", "expiration_date", "bond_expiration", "insurance_expiration", "Categories", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses"]

f.write("|".join(headers) + "\n")

#*************************** Get Active Companies ****************************************

def main():
	for i in range(0, 5001): #5001

		try:

			url = "https://agriculture.tn.gov/ListCharter.asp?ACTION=DETAIL&ID=%d" % i
			page = requests.get(url)
			soup = BeautifulSoup(page.content.replace('<BR>', '|'))

			info = []

			for tr in soup.find_all('tr')[1:13]:

				td = tr.find_all('td')
		
				info.append(re.sub("\xa0"," ",td[0].text))
		
			for tr in soup.find_all('table')[1].find_all('tr')[1:]:
				for td in tr.find_all('td'):
					info.append(re.sub("\xa0"," ",td.text))

		
			f.write("|".join(info) + "\n")
		
			print "|".join(info) + "\n" 
			print '*' * 50
		
			info=[]
			
		except Exception as e:
			print str(e)
			print '*' * 50
			continue

if __name__ == '__main__':
    main()
'''
There does not seem to be any distinction between "expired" and "non expired" Companies (anymore 1/26 - 1/30)
#************************** Get Expired Companies ****************************************

for j in range(0, 100):

	try: 
		# Expired companies have a slightly different url. Note the 'E' at the end.
		url = "https://agriculture.tn.gov/ListCharter.asp?ACTION=DETAIL&ID=%dE" % j
		page = requests.get(url)
		soup = BeautifulSoup(page.content.replace('<BR>', '|'))

		info = []

		for tr in soup.find_all('tr')[1:13]:

			td = tr.find_all('td')
	
			info.append(re.sub("\xa0"," ",td[0].text))
	

		for tr in soup.find_all('table')[1].find_all('tr')[1:]:
			for td in tr.find_all('td'):
			
				info.append(re.sub("\xa0"," ",td.text))

	
		f.write("\"" + "\",\"".join(info) + "\"\n")
	
		print "\"" + "\",\"".join(info) + "\"\n" 
		print '*' * 50
		
		info=[]
		
	except Exception as e:
		print str(e)
		print '*' * 50
		continue
'''
f.close()
	



		







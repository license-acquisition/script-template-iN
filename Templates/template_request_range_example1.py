import csv, codecs, requests, time #optional: re, string
from bs4 import BeautifulSoup
from script_template import create_file
from script_template import log

def main():
	#### standardized code
	time_stamp = time.strftime("%Y%m%d")
	#type = asb,hva, etc.. authority = OKepa etc. entity_type = c, i, or b
	f = codecs.open("pes_c_TNdoa_%s_000.csv" % time_stamp, "w","UTF-8")
	#Always use canonical headers
	headers = ["license_number", "entity_name", "address1", "address2", "city,state,zip", "phone", "first_issue_date", "last_renew_date", "expiration_date", "bond_expiration", "insurance_expiration", "Categories", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses", "ID#", "qualifying_individual", "Address", "Certifications", "Licenses"]
	f.write("|".join(headers) + "\n")
	headers = get_headers([21,12,0,1,"ctiy,state,zip",])

	start = 0 #change start and end
	end = 5001
	###application logic
	try:
		for i in range(start, end):
			bbb
			try:
				url = "https://agriculture.tn.gov/ListCharter.asp?ACTION=DETAIL&ID=%d" % i
				page = requests.get(url)
				soup = BeautifulSoup(page.content.replace('<BR>','|'))
				info = []
				
				for tr in soup.find_all('tr')[1:13]:
					td = tr.find_all('td')

					info.append(td[0].text.replace(u'\xa0',u''))
				for tr in soup.find_all('table')[1].find_all('tr')[1:]:
					for td in tr.find_all('td'):
						info.append(td.text.replace(u'\xa0',u''))

				f.write("|".join(info) + "\n")
				print "|".join(info) + "\n"
			except Exception, e:
				print str(e)
				#optional: add other things to do when you fail
				continue
	except Exception, e:
		print str(e)
	finally:
		f.close()
			
if __name__ == '__main__':
	main()
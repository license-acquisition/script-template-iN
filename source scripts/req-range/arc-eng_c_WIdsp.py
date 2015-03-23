'''
Christopher Jimenez
3/2/2015
https://app.wi.gov/LicenseSearch/OrganizationLicense/SearchResultsSummary?chid=71629

range was found by troubleshooting. try adjusting range in the browser beyond 74424

'''
import requests, codecs, time
from bs4 import BeautifulSoup

f = codecs.open('arc-eng_c_WIdsp_%s_000.csv' % time.strftime('%Y%m%d'),'w','UTF-8')
headers = ['entity_name','license_type','license_number','city','status','expiration_date','issue_date','speciality']
f.write("|".join(headers) +"\n")

for i in range(71629,74424):
	print i
	page = requests.get('https://app.wi.gov/LicenseSearch/OrganizationLicense/SearchResultsSummary?chid=%d' % i)
	soup = BeautifulSoup(page.content)
	info = []
	paragraphs = soup.find_all('p')
	org_information = paragraphs[1]
	for strong in org_information.find_all('strong'):
		strong.extract()
	a = org_information.text.split('\n')
	
	info.append(a[1].strip().replace(u'\xd6',u' '))
	info.append(a[2].strip().replace(u'\xd6',u' '))
	info.append(a[3].strip().replace(u'\xd6',u' '))
	info.append(a[4].strip().replace(u'\xd6',u' '))
	info.append(a[6].strip().replace(u'\xd6',u' '))
	license_information = paragraphs[2]
	for strong in license_information.find_all('strong'):
		strong.extract()
	b = license_information.text.split('\n')
	info.append(b[1].strip().replace(u'\xd6',u' '))
	info.append(b[2].strip().replace(u'\xd6',u' '))
	info.append(b[5].strip().replace(u'\xd6',u' '))
	print '|'.join(info)
	f.write('|'.join(info) + '\n')
pdf
	soup.decompose()
f.close()	
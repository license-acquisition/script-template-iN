'''
Christopher Jimenez
3/2/2015
https://app.wi.gov/LicenseSearch/OrganizationLicense/SearchResultsSummary?chid=71629

range was found by troubleshooting. try adjusting range in the browser beyond 74424

'''
import requests, codecs, time
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('arc-eng_c_WIdsp', 'w', ['12', 'license_type', '21', '4', '37', '13', '19', 'speciality'])
l = logger('arc-eng_c_WIdsp')

def main():
	for i in range(71629,74424):
		try:
			soup = BeautifulSoup(requests.get('https://app.wi.gov/LicenseSearch/OrganizationLicense/SearchResultsSummary?chid=%d' % i).content)
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
			l.info(info)
			f.write('|'.join(info) + '\n')
			soup.decompose()
		except Exception as e:
			l.error(str(e))

if __name__ == '__main__':
	try:
        main()
        l.info('complete')
    except Exception as e: l.critical(str(e))
    finally: f.close()
'''
Christopher jimenez

http://www.firemarshal.alabama.gov/Reports/PrintAllSprinklers.aspx
'''

import time, requests, codecs
from bs4 import BeautifulSoup

def sprinkler():
	f = codecs.open('fir.b_c_ALfmo_%s_000.csv'%time.strftime('%Y%m%d'),'w')
	headers = ['entity_name','address1','phone','license_number','status','first_issue_date','expiration_date','qualified_individual']
	f.write("\"" + "\"|\"".join(headers) + "\"\n")
	page = requests.get('http://www.firemarshal.alabama.gov/Reports/PrintAllSprinklers.aspx')
	soup = BeautifulSoup(page.content)
	tds = soup.find_all('td')
	for i in range(0, len(tds), 8):
		info = []
		info.append(tds[0 + i].text)
		info.append(tds[1 + i].text)
		info.append(tds[2 + i].text)
		info.append(tds[3 + i].text)
		info.append(tds[4 + i].text)
		info.append(tds[5 + i].text)
		info.append(tds[6 + i].text)
		info.append(tds[7 + i].text)
		f.write("\"" + "\"|\"".join(info) + "\"\n")
		print "\"" + "\"|\"".join(info) + "\"\n"
	f.close()

def alarm():
        f = codecs.open('fir.a_c_ALfmo_%s_000.txt'%time.strftime('%Y%m%d'),'w', 'utf-8')
        headers = ['company_name','address1','phone','license_number','status', 'CertificationHolder', 'HolderStatus', 'LicensedAs', 'issue_date','expiration_date']
        f.write("|".join(headers) + "\n")
        page = requests.get('http://www.firemarshal.alabama.gov/Reports/PrintAllFireAlarm.aspx')
        time.sleep(5)
        soup = BeautifulSoup(page.content)
        time.sleep(5)
        tds = soup.find_all('td')
        print len(tds)
        for i in range(0, len(tds), 11):
                info = []
                info.append(tds[1 + i].text)
                info.append(tds[2 + i].text)
                info.append(tds[3 + i].text)
                info.append(tds[4 + i].text)
                info.append(tds[5 + i].text)
                info.append(tds[6 + i].text)
                info.append(tds[7 + i].text)
                info.append(tds[8 + i].text)
                info.append(tds[9 + i].text)
                info.append(tds[10 + i].text)
                f.write("|".join(info) + "\n")
                print info
        f.close()

if __name__ == "__main__":
        #sprinkler()
        alarm()

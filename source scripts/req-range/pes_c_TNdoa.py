#********************
# Tennessee Department of Agriculture Pest Control Scrape
# @author Anthony Nault
# @contributor Chris Jimenez
# 07/09/2014
# edited 01/26/2015
#********************

import csv, re, requests, time
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('pes_c_TNdoa', 'w', [21,12,0,1,"ctiy,state,zip",])
l = logger('pes_c_TNdoa')

#*************************** Get Active Companies ****************************************

def main():
	for i in range(0, 5001): #5001
		try:
			url = "https://agriculture.tn.gov/ListCharter.asp?ACTION=DETAIL&ID=%d" % i
			soup = BeautifulSoup(requests.get(url).content.replace('<BR>', '|'))

			info = []
			for tr in soup.find_all('tr')[1:13]:
				td = tr.find_all('td')		
				info.append(re.sub("\xa0"," ",td[0].text))		
			for tr in soup.find_all('table')[1].find_all('tr')[1:]:
				for td in tr.find_all('td'):
					info.append(re.sub("\xa0"," ",td.text))

			f.write("|".join(info) + "\n")
		
			l.info(info)
		
			info=[]
			
		except Exception as e:
			l.error('Error on %s: %s' %(i,str(e)))

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()

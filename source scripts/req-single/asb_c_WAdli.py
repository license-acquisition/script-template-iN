#********************
# Washington Labor and Industry Asbestos Certification Scrape
# Anthony Nault
# 7/10/2014
#********************

import csv, re, requests, time
from bs4 import BeautifulSoup
from script_template import create_file, logger

#********************* Name the File You Want to Put Your Data Into **********************

f = create_file('asb_c_WAdli', 'w', ['12', '0', '1', '11', '35', '33', '66', '21', '13'])
l = logger('asb_c_WAdli')
 
def main():
	#******************************* Get URL to Scrape ***************************************

	url = "http://www.lni.wa.gov/Safety/Topics/AtoZ/Asbestos/contractorlist.asp"
	soup = BeautifulSoup(requests.get(url).content.replace('<br />', '|'))

	#********************************* Parse HTML ********************************************

	trs = soup.find_all('tr')[2:]

	for tr in trs:
		info = []	

		for td in tr.find_all('td'):		
			rows = td.text.split('|')
			m = len(rows)
			
			# Modify length of rows to preserve alignment in the CSV
			if tr.find_all('td').index(td) == 0:	
				if m < 4:
					while m < 4:	
						rows.append("")
						m = len(rows)							
			if tr.find_all('td').index(td) == 1:	
				if m < 3:
					while m < 3:	
						rows.append("")
						m = len(rows)			
			if tr.find_all('td').index(td) == 2:
				if m < 2:
					while m < 2:
						rows.append("")
						m = len(rows)
					
			for data in rows:
				data = re.sub('\xa0',"",data)
				data = re.sub('\s\s*'," ",data)

				info.append(data)		
		
		f.write("|".join(info) + "\n")	
		l.info(info)

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
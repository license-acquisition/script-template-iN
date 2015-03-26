#
# Chris Jimenez 
# 02/10/2015
# http://opc.deq.state.ms.us/report_lead_el.aspx

import sys, requests, codecs, re, csv, time
from bs4 import BeautifulSoup
from selenium import webdriver
from script_template import create_file, logger

f = create_file('led_c_MSdeq', 'w', [12, 0, 8, 33, 32, 21, 13])
l = logger('MSdeq')
driver = webdriver.PhantomJS()

def main():
	driver.get('http://opc.deq.state.ms.us/report_lead_el.aspx')
	values = ['PBF','PDT','NBF','PBI','PPD','PBR','PRA','PBS','PBW']
	#for _b_ use range 0,9
	for i in range (0,3):
		try:
			driver.find_element_by_css_selector('option[value='+values[i]+']').click()
			driver.find_element_by_id('uxSubmit').click()
			time.sleep(3)
			soup = BeautifulSoup(driver.page_source)
			for br in soup.findAll('br'):
				br.extract()
			table = soup.find('table',{'class':'resultbox'})
			tds = table.findAll('td')[7:]
			l.debug(str(len(tds) / 7))
			for i in range(0,len(tds)/7):
				info = []
				info.append(tds[0 + i * 7].text.strip())
				
				info.append(tds[1 + i * 7].text.strip())
				
				info.append(tds[2 + i * 7].text.strip())
				
				info.append(tds[3 + i * 7].text.strip())
				
				info.append(tds[4 + i * 7].text.strip())
				
				info.append(tds[5 + i * 7].text.strip())
				
				info.append(tds[6 + i * 7].text.strip())
				
				f.write('\"' + "\"|\"".join(info) + "\"\n")
				
				l.info('\"' + "\",\"".join(info) + "\"\n")
		except Exception as e:
			l.error(str(e))
			pass

if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception as e:
		l.critical(str(e))
	finally:
		f.close()
		driver.quit()
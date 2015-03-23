#
# Chris Jimenez 
# 02/10/2015
# http://opc.deq.state.ms.us/report_lead_el.aspx

import sys, requests, codecs, re, csv, time
from bs4 import BeautifulSoup
from selenium import webdriver



headers = ['entity_name','address1','county','phone','license_type','licnese_number','expiration_date']
values = ['PBF','PDT','NBF','PBI','PPD','PBR','PRA','PBS','PBW']
f = codecs.open('led_c_MSdeq_%s_000.csv' % str(time.strftime('%Y%m%d')), 'w','UTF-8')
f.write('\"' + "\"|\"".join(headers) + "\"\n")
browser = webdriver.Chrome()
browser.get('http://opc.deq.state.ms.us/report_lead_el.aspx')


#for _b_ use range 0,9
for i in range (0,3):
	try:
		browser.find_element_by_css_selector('option[value='+values[i]+']').click()
		browser.find_element_by_id('uxSubmit').click()
		time.sleep(3)
		soup = BeautifulSoup(browser.page_source)
		for br in soup.findAll('br'):
			br.extract()
		table = soup.find('table',{'class':'resultbox'})
		tds = table.findAll('td')[7:]
		print len(tds) / 7
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
			
			print '\"' + "\",\"".join(info) + "\"\n"
	except Exception as e:
		print e
		pass

f.close()
browser.close()
browser.quit()


'''
Chris Jimenez
adjust number of tabs based on "pages" found on the view list page.

'''
import time, codecs, requests
from bs4 import BeautifulSoup
from selenium import webdriver

def main():
	
	#start section 1
	f = codecs.open('plu_b_MIbcc_links.csv','w','UTF-8')
	driver = webdriver.PhantomJS()
	driver.get('http://w3.lara.state.mi.us/bcclicense/Search.asp')
	driver.find_element_by_css_selector('#mainform > table > tbody > tr:nth-child(1) > td:nth-child(4) > select > option:nth-child(22)').click()
	driver.find_element_by_css_selector('#mainform > table > tbody > tr:nth-child(5) > td > input[type="submit"]:nth-child(1)').click()
	num_tabs = 158 #adjust number of tabs based on "pages" found on the view list page.
	for i in range(1,num_tabs + 1):
		soup = BeautifulSoup(driver.page_source)
		table = soup.find('table',{'id':'display_info'})
		links = table.find_all('a')
		for i in range(0, len(links), 2):
			f.write(links[i]['href'] + '\n')
			print "acquiring link " + links[i]['href']
		if i != num_tabs:
			driver.find_element_by_css_selector('body > table:nth-child(5) > tbody > tr > td > table:nth-child(2) > tbody > tr > td > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(8) > td > input[type="button"]:nth-child(4)').click()
	f.close()
	driver.close()
	driver.quit()
	#end section 1


	#start section 2
	headers = ['entity_name','qualified_individual','city','state','zip','qualified_individual','licnese_type','license_number','status','expiration_date']
	l = open('plu_b_MIbcc_links.csv', 'r')
	g = codecs.open('plu_b_MIbcc_%s_000.csv'%time.strftime('%Y%m%d'),'w','UTF-8')
	g.write("|".join(headers) + "\n")
	for link in l:
		info = []
		page = requests.get('http://w3.lara.state.mi.us/bcclicense/' + link)
		soup = BeautifulSoup(page.content)
		tds = soup.find_all('td')
		qualified1_individual = tds[14].text.replace(u'\xa0',u'').strip()
		entity_name = tds[15].text.replace(u'\xa0',u'').strip()
		address = tds[17]
		address.find('b').extract()
		address = address.text.replace(u'\xa0',u'').strip()
		zipcode = address[-5:]
		state 	= address[-8:-6]
		city = address[:-9]
		qualified_individual = tds[18]
		qualified_individual.find('b').extract()
		qualified_individual = qualified_individual.text.replace(u'\xa0',u'').strip()
		license_number = tds[24].text.replace(u'\xa0',u'').strip()
		license_type = tds[25].text.replace(u'\xa0',u'').strip()
		status 	= tds[29].text.replace(u'\xa0',u'').strip()
		expiration_date = tds[30].text.replace(u'\xa0',u'').strip()

		info.append(entity_name)
		info.append(qualified1_individual.replace(u',',u''))
		info.append(city)
		info.append(state)
		info.append(zipcode)
		info.append(qualified_individual.replace(u',',u''))
		info.append(license_number)
		info.append(license_type)
		info.append(status)
		info.append(expiration_date)
		g.write("|".join(info) + "\n")
		print "|".join(info) + "\n"
	l.close()
	g.close()
	#end section 2


if __name__ == '__main__':
	main()
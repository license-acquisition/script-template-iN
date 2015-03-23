import sys, re, requests, codecs, csv
from bs4 import BeautifulSoup
from selenium import webdriver

f = codecs.open('pes_i_WIatc_20140722.csv', 'w', 'utf-8')
g = open("pes_i_WIatc_links.txt", "w")
browser = webdriver.PhantomJS()
browser.get("http://www.kellysolutions.com/WI/Business/searchbyCity.asp")

j=0
while j < 100:
	browser.find_elements_by_css_selector("option")[j].click()
	browser.find_element_by_css_selector("input[value='Search for the selected criteria']").click()
	while True:
		try:
			soup = BeautifulSoup(browser.page_source)
			for link in soup.find_all('a'):
				#print link
				if "showcoinfo" in link['href']:
					g.write("http://www.kellysolutions.com/WI/Business/%s\n"%link['href'])
					"""soup2 = BeautifulSoup(requests.get("http://www.kellysolutions.com/wv/Applicators/%s"%link['href']).content.replace("&nbsp;", " "))
					try:

						data = []
						data.append((re.search("NEB[0-9]{6}",soup2.text).group()))
						data.append((re.search("\d{1,2}[/]\d{1,2}[/]\d{4}",soup2.text).group()))
						data.append(soup2.find_all("p", {"style" : "margin-top: 0; margin-bottom: 0"})[4].text.replace("\r", "").replace("\n", ""))
						data.append(soup2.find_all("td", {"width" : "82%"})[0].text.replace("\r", " ").replace("\n", " "))
						data.append(soup2.find_all("td", {"width" : "82%"})[1].text.replace("\r", " ").replace("\n", " "))
						data.append(soup2.find_all("td", {"width" : "82%"})[2].text.replace("\r", " ").replace("\n", " "))
						data.append(soup2.find_all("td", {"width" : "82%"})[3].text.replace("\r", " ").replace("\n", " "))
						data.append(soup2.find_all("td", {"width" : "77%"})[0].text.strip().replace("\r", " ").replace("\n", "\",\""))
						
						data[5] = re.sub("  *", " ", data[5]).strip()
						data[5] = "\",\"".join(data[5].rsplit(" ", 2))

						#print('\"' + "\",\"".join(data) + "\"\n")
						f.write('\"' + "\",\"".join(data) + "\"\n")


					#print soup2.prettify()	
					except Exception as e:
						print str(e)
						print j"""
			browser.find_element_by_css_selector("input[value='  >   ']").click()
		except:
			print "Next list %d"%j
			j=j+1
			print j
			break
			



import codecs, re, csv, time, requests
from bs4 import BeautifulSoup
from selenium import webdriver

f = codecs.open('gen.res_c_NDsos_%s_000.csv'%time.strftime('%Y%m%d'), 'w', 'utf-8')
s = requests.session()
browser = webdriver.PhantomJS()
j=0
i=1
while i < 54: # county search
	browser.get("https://apps.nd.gov/sc/busnsrch/busnSearch.htm?results=false")
	browser.find_element_by_css_selector("option[value='%02d']"%i).click()
	browser.find_element_by_css_selector("input[value='Search']").click()
	soup = BeautifulSoup(browser.page_source)
	print i
	while True:
		for tr in soup.find("table", {"cellspacing" : "1", "summary" : "Businesses returned in search results"}).find_all("tr")[1:]:
			data={"submitType":"submitDetail", "submitID":tr.find("td").text, "submitEntityType":"Contractor"}
			soup = BeautifulSoup(s.post("https://apps.nd.gov/sc/busnsrch/busnSearch.htm#Search_Results", data=data).content)
			try:				
				payload = []
				for strong in soup.find("div", {"class" : "content"}).find_all("strong")[:-1]:
					strong.decompose()
				payload.append(soup.find("div", {"class" : "content"}).find("h3").text.replace(u'\xa0',u''))
				for li in soup.find("table", {"cellspacing" : "0", "summary" : "Entity details"}).find_all("li"):
					payload.append(li.text.replace(u'\xa0',u''))
				for span in soup.find_all("div", {"class" : "address"})[0].find_all("span"):
					payload.append(span.text.replace(u'\xa0',u''))
				for span in soup.find_all("div", {"class" : "address"})[1].find_all("span"):
					payload.append(span.text.replace(u'\xa0',u''))
				try:	
					for span in soup.find_all("div", {"class" : "address"})[2].find_all("span"):
						payload.append(span.text.replace(u'\xa0',u''))
				except:
					pass
			except Exception as e:
				print str(e)
			f.write('\"' + "\",\"".join(payload) + "\"\n")
			print payload
			j+=1
	
		try:
			browser.find_element_by_link_text("Next").click()
			time.sleep(2)
			soup = BeautifulSoup(browser.page_source)
		except:
			break

	i=i+1

f.close()
browser.close()
browser.quit()

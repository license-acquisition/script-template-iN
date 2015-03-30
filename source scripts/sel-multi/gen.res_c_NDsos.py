import codecs, re, csv, time, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from script_template import create_file, logger

f = create_file('gen.res_c_NDsos', 'w', [])
l = logger('gen.res_c_NDsos')
s = requests.session()
driver = webdriver.PhantomJS()

def main():
	j=0
	i=1
	while i < 54: # county search
		driver.get("https://apps.nd.gov/sc/busnsrch/busnSearch.htm?results=false")
		driver.find_element_by_css_selector("option[value='%02d']"%i).click()
		driver.find_element_by_css_selector("input[value='Search']").click()
		soup = BeautifulSoup(driver.page_source)
		l.debug(i)
		while True:
			for tr in soup.find("table", {"cellspacing" : "1", "summary" : "Businesses returned in search results"}).find_all("tr")[1:]:
				data={"submitType":"submitDetail", "submitID":tr.find("td").text, "submitEntityType":"Contractor"}
				soup = BeautifulSoup(s.post("https://apps.nd.gov/sc/busnsrch/busnSearch.htm#Search_Results", data=data).content)
				try:				
					info = []
					for strong in soup.find("div", {"class" : "content"}).find_all("strong")[:-1]:
						strong.decompose()
					info.append(soup.find("div", {"class" : "content"}).find("h3").text.replace(u'\xa0',u''))
					for li in soup.find("table", {"cellspacing" : "0", "summary" : "Entity details"}).find_all("li"):
						info.append(li.text.replace(u'\xa0',u''))
					for span in soup.find_all("div", {"class" : "address"})[0].find_all("span"):
						info.append(span.text.replace(u'\xa0',u''))
					for span in soup.find_all("div", {"class" : "address"})[1].find_all("span"):
						info.append(span.text.replace(u'\xa0',u''))
					try:	
						for span in soup.find_all("div", {"class" : "address"})[2].find_all("span"):
							info.append(span.text.replace(u'\xa0',u''))
					except:
						pass
				except Exception as e:
					l.error(str(e))
				f.write("|".join(info) + "\n")
				l.info(info)
				j+=1
		
			try:
				driver.find_element_by_link_text("Next").click()
				time.sleep(2)
				soup = BeautifulSoup(driver.page_source)
			except:
				break

		i=i+1

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
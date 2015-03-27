from selenium import webdriver
import requests
import codecs, time, re
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('sec_c_MIcsc', 'w', ['6', 'url', '12', '35', '0', '8', '32', '21', '78', '37', '76', '19', '13', 'employer_manager', 'employer_license_number', 'employer_address', '8'])
l = logger('sec_c_MIcsc')
g = codecs.open('sec_c_MIcsc_links.csv', 'w', 'utf-8')
driver = webdriver.PhantomJS()

def main():
	driver.get("https://www.lara.michigan.gov/colaLicVerify/lName.jsp")
	driver.find_element_by_xpath("//*[@id='radio2']").click()
	driver.find_element_by_xpath("//*[@id='orgName']").send_keys("%")
	driver.find_element_by_xpath("//*[@id='professions']/option[25]").click()
	driver.find_element_by_xpath("/html/body/form/table[3]/tbody/tr/td/input").click()
	x=1
	while x < 1760:
		for link in BeautifulSoup(driver.page_source).findAll("a"):
			if "detailType=Company" in link['href']:
				l.info(link['href'])
				g.write(link['href'] + "\n")
			else:
				pass
		driver.find_element_by_xpath("//*[@id='%sa']"%x).click()
		x = x+1

	s = requests.session()
	s.get("https://www.lara.michigan.gov/colaLicVerify/lName.jsp")

	for line in open("MIlar_links_test.csv","r"):
		try:
			url = "https://www.lara.michigan.gov/colaLicVerify/" + line.strip()
			source = s.get(url)
			soup = BeautifulSoup(source.content.replace("</br>","_"))
			info = []
			info.append("1")
			info.append(line.strip())
			info.append(soup.findAll("table",{"class":"table1"})[0].findAll("td")[2].text.strip())
			info.append(soup.findAll("table",{"class":"table1"})[0].findAll("td")[6].text.strip())
			info.append(soup.findAll("table",{"class":"table1"})[0].findAll("td")[-3].text.strip())
			info.append(soup.findAll("table",{"class":"table1"})[0].findAll("td")[-1].text.strip())
			info.append(soup.findAll("table",{"class":"table1"})[1].findAll("td")[2].text.strip())
			info.append(soup.findAll("table",{"class":"table1"})[1].findAll("td")[4].text.strip())
			info.append(re.sub("\s+","",soup.findAll("table",{"class":"table1"})[1].findAll("td")[6].text))
			info.append(soup.findAll("table",{"class":"table1"})[1].findAll("td")[8].text.strip())
			info.append(soup.findAll("table",{"class":"table1"})[1].findAll("td")[-7].text.strip()) #limitations
			info.append(soup.findAll("table",{"class":"table1"})[1].findAll("td")[-5].text.strip()) #issue
			info.append(soup.findAll("table",{"class":"table1"})[1].findAll("td")[-3].text.strip()) #exp
			info.append(soup.findAll("table",{"class":"table1"})[2].findAll("td")[2].text.strip())
			info.append(soup.findAll("table",{"class":"table1"})[2].findAll("td")[4].text.strip())
			info.append(soup.findAll("table",{"class":"table1"})[2].findAll("td")[-3].text.strip())
			info.append(soup.findAll("table",{"class":"table1"})[2].findAll("td")[-1].text.strip())
			l.info(info)
			f.write("\"" + "\"|\"".join(info) + "\"\n")
		except Exception as e:
			l.error("Parsing/Connection Error", info)
			l.error(str(e))

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
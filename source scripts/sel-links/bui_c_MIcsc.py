from selenium import webdriver
import requests
import codecs, time, re
from bs4 import BeautifulSoup
#browser = webdriver.PhantomJS()
f = codecs.open("gen.res_c_MIcsc_%s_000.csv"%(time.strftime("%Y%m%d")),"w","utf-8")
f.write("company_flag|url|entity_name|qualifying_individual|address|county|licensee_type_cd|license_number|specialties|status|limiations|issue_date|expiration_date|employer_manager|employer_license_number|employer_address|county\n")
l = codecs.open("gen.rs_c_MIlar_audit.csv","w","utf-8")
'''
link_list = open("MIlar_links_test.csv","a")
browser.get("https://www.lara.michigan.gov/colaLicVerify/lName.jsp")
browser.find_element_by_xpath("//*[@id='radio2']").click()
browser.find_element_by_xpath("//*[@id='orgName']").send_keys("%")
browser.find_element_by_xpath("//*[@id='professions']/option[25]").click()
browser.find_element_by_xpath("/html/body/form/table[3]/tbody/tr/td/input").click()
x=1
while x < 1760:
	for link in BeautifulSoup(browser.page_source).findAll("a"):
		if "detailType=Company" in link['href']:
			print link['href']
			link_list.write(link['href'] + "\n")
		else:
			pass
	browser.find_element_by_xpath("//*[@id='%sa']"%x).click()
	x = x+1
	print x
browser.close()
browser.quit()
'''
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
		print "\"" + "\"|\"".join(info) + "\"\n"
		f.write("\"" + "\"|\"".join(info) + "\"\n")
	except:
		print "Parsing/Connection Error", info
		l.write(str(url) + "\n")
f.close()
l.close()

import requests, codecs, time
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date
start = time.time()
f = codecs.open('led_c_KSdoh_%s_000.csv' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
f.write("company_flag|state|county|city|entity_name|address1|phone|license_number|licensee_type_cd|licensee_type_cd|name\n")
browser = webdriver.Chrome()
browser.get("http://kensas.kdhe.state.ks.us/leadRegistry/getActiveLeadRegistryFirmSearchForm.kdhe")
info = []
browser.find_elements_by_tag_name("input")[1].click()
browser.find_elements_by_tag_name("input")[-1].click()
for tr in BeautifulSoup(browser.page_source.replace("<br />", "_%_").replace("</b>","").replace("<br>","_%_")).find("table", {"border":"2"}).findAll("tr")[1:]:
	info.append("1")	
	for td in tr.findAll("td"):
		info.append(td.text.replace("\"", "").replace("_%_", "\",\"").replace("&amp;", "&").replace("\n", "").strip())

	#print "\"" + "\"|\"".join(info) + "\"\n"
	f.write("\"" + "\"|\"".join(info) + "\"\n")
	info = []
print time.time()-start

browser.close()
f.close()
browser.quit()

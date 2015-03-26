import requests, codecs, time
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('led_c_KSdoh', 'w', ['6', '36', '8', '4', '12', '0', '33', '21', '32', '32', '35'])
l = logger('led_c_KSdoh')

info = []
s = requests.Session()
s.get('http://kensas.kdhe.state.ks.us/leadRegistry/getActiveLeadRegistryFirmSearchForm.kdhe')
page = s.get('http://kensas.kdhe.state.ks.us/leadRegistry/getActiveLeadRegistryFirms.kdhe?firmSearchType=listAll')
time.sleep(5)
for tr in BeautifulSoup(page.content.replace("<br/>", "_%_").replace("<br>","_%_").replace('<br />', '_%_')).find_all('tr', {'valign': 'top'}):
	#print tr
	info.append("1")	
	for td in tr.findAll("td"):
		try:
			data = td.text.split('_%_')
			for d in data:
				info.append(d.replace('\n','').replace('\t','').replace('\r','').strip())
		except:
			info.append(td.text.replace("\"", "").replace("&amp;", "&").replace("\n", "").replace('\t','').replace('\r','').strip())
	l.info(info)
	f.write('|'.join(info) + '\n')
	info = []

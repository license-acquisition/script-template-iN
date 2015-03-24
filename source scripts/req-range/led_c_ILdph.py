import codecs, re, requests, csv, time, sys
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('led_c_ILdph', 'w', ['32', '102', '21', '12', 'last update', '8', '0', '4', '36', '44', '13', '33', '66'])
l = logger('led_c_ILdph')

def main():
	s = requests.session()
	found = True
	for i in xrange(1,999999999,20):
		if found == False:
			break
		found = False
		url = "http://app.idph.state.il.us/envhealth/lead/LeadListing.asp?list=contractors&NoRec=20&Go=Go"
		page = s.get(url)
		page = s.get("http://app.idph.state.il.us/envhealth/lead/genericdb/code/GenericList.asp?START=" + str(i))
		soup = BeautifulSoup(page.content)

		for link in soup.find_all("a"):
				try:
					if 'GenericView' in link['href']:
						found = True
						soup= BeautifulSoup(s.get("http://app.idph.state.il.us" + link["href"]).content)
						#print soup.text
						info = []
						info.append("Licensed Lead Contractors")
						info.append("License Number")
						table = soup.find_all("table", {"cellpadding" : "2"})[1]
						for tr in table.find_all("tr"):
							info.append(re.sub("\s+", " ", tr.find_all("td")[1].text.strip().replace(u',',' ')))
						l.info(info)
						f.write("|".join(info) + "\n")
				except Exception as e:
					l.error('Error on %s: %s' %(i,str(e)))

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
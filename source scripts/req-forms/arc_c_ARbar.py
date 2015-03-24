import codecs, re, requests, csv, time
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('arc_c_ARbar', 'w', ['21', '6', '0', '4', '36', '44', '37', '13', '102', '32'])
l = logger('arc_c_ARbar')

def main():
	url = "https://www.ark.org/asbalaid/index.php/arch/search_firm"
	soup = BeautifulSoup(requests.get(url).content)

	i=0
	for option in soup.find("select", {"name" : "state"}).find_all("option")[1:]:
		urlnext = "https://www.ark.org/asbalaid/index.php/arch/search_firm?license_num=&name=&city=&state=" + option['value'] + "&submit=Search%21" 
		soupnext = BeautifulSoup(requests.get(urlnext).content)
		for link in soupnext.find_all("a"):
			try:
				if 'details' in link['href']:
					souplast = BeautifulSoup(requests.get(link['href']).content)
					info = []
					for tr in souplast.find("table", {"class" : "table"}, {"width" : "75%"}).find_all("tr"):
						for td in tr.find_all("td")[1:]:
							info.append(td.text)
					info.append(souplast.find_all("div", {"class" : "row-fluid"}, {"align" : "center"})[1].find("strong").text)
					for link in souplast.find_all("a"):
						try:
							if 'certificate_firm' in link['href']:
								pagecert = requests.get(link['href'])
								soupcert = BeautifulSoup(pagecert.content)
								info.append(soupcert.find_all("p", {"align" : "center"})[0].find("strong").text.replace("This individual registration expires on ", ""))
						except Exception, e:
							l.error(str(e))
					while len(info) < 8:
						info.append("")
					info.append("Certificate of Authorization Number")
					info.append("Architectural Firm")								
					f.write('|'.join(info) + '\n')
					l.info(info)
			except Exception, e:
				l.error(str(e))
		i=i+1		

if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception, e: l.critical(str(e))
	finally: f.close()
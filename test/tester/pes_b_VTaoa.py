import requests, re
from bs4 import BeautifulSoup
from script_template import create_file, logger


f = create_file("pes_b_VTaoa","w",[21,12,0,1,4,36,44,32,13,22,14])


s = requests.session()

def parse(bsObject):
	for a in bsObject.findAll("a"):
		try:
			if "showcoinfo" in a['href']:
				bsPage = BeautifulSoup(requests.get("http://www.kellysolutions.com/VT/Applicators/%s"%a['href']).content)
				
				info = []
				info.append(re.match(".*Applicator ID:([0-9]*-[0-9]*)", bsPage.text.replace(u'\xa0',u'').replace(u'\n', u'').replace(u'\r',u'')).group(1).strip())
				for td in bsPage.findAll("td", {"width":"82%"}):
					info.append(td.text.replace(u'\xa0', u' ').replace(u'\r',u'').replace(u'\n',u'').strip())
				for td in bsPage.findAll("table")[2].findAll("td")[1:]:
					info.append(td.text.replace("(expires", "\"|\"").replace(")", "\"|\"").replace(u'\xa0', u'').replace(u'\r',u'').replace(u'\n',u'').strip())
			
				info[4] = "\"|\"".join(info[4].replace(",","").split('   '))
				f.write("|".join(info) + "\n")
				l.info("\"" + "\"|\"".join(info) + "\"\n")

		except Exception, e:
			l.error(str(e))
def main():
	for applicatorType in ["C", "N"]:
		for letter in ["a", "e", "i", "o", "u"]:
			soup = BeautifulSoup(s.post("http://www.kellysolutions.com/VT/Applicators/searchbyconame.asp", {"LastName":"%s"%letter,"ApplicatorType":"%s"%applicatorType}).content)

			parse(soup)
			matching_applicators = soup.findAll('p')[1]
			matching_applicators.find('b').extract()
			
			for i in range(1, int(matching_applicators.text.replace(u'\xa0',u''))/100):
				
				parse(BeautifulSoup(s.post("http://www.kellysolutions.com/VT/Applicators/searchbyconame.asp", {"LastName":"%s"%letter,"ApplicatorType":"%s"%applicatorType,"fpdbr_0_PagingMove":"  >   "}).content))


if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		l.critical(str(e))
	finally:
		f.close()

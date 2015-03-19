import requests#optional: re, string
from bs4 import BeautifulSoup
from script_template import create_file

f = create_file('pro-type_entity-type_authority','w',[21,12,0,1,"ctiy,state,zip"])

def main():

	start = 0 #change start and end
	end = 5001
	###application logic
	
	for i in range(start, end):
		try:
			url = "https://agriculture.tn.gov/ListCharter.asp?ACTION=DETAIL&ID=%d" % i
			page = requests.get(url)
			soup = BeautifulSoup(page.content.replace('<BR>','|'))
			info = []
			
			for tr in soup.find_all('tr')[1:13]:
				td = tr.find_all('td')

				info.append(td[0].text.replace(u'\xa0',u''))
			for tr in soup.find_all('table')[1].find_all('tr')[1:]:
				for td in tr.find_all('td'):
					info.append(td.text.replace(u'\xa0',u''))

			f.write("|".join(info) + "\n")
			print "|".join(info) + "\n"
		except Exception, e:
			print str(e)
			#optional: add other things to do when you fail
			continue

			
if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		print str(e)
	finally:
		f.close()

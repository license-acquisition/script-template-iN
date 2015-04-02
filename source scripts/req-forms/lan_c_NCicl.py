################################
# feed: lan_c_NCicl
# type: request, form
################################

import requests
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('lan_c_NCicl', 'w', ['7', '21', '35', '7', '0', 'City/State/Zip', '8', '33', '66', '11', '43'])
l = logger('lan_c_NCicl')

def main():
	try:
		page = 1
		while True:
			l.debug('Searching page %s' %page)
			url = 'http://www.nciclb.org/licensees/licensees-corporate/page/%s/' %page
			soup = BeautifulSoup(requests.get(url).content.replace('<br/>','|').replace('<br />','|'))
			trs = soup.find_all('tr')[1:]
			for i in range(0, len(trs), 2):
				info = []
				for td in trs[i].find_all('td'):
					info.append(td.text.replace('\n',''))
				for p in trs[i+1].find_all('p'):
					data = p.text.split('|')
					data = [x.replace('\n','').strip() for x in data]
					for dt in data:
						info.append(dt)
				info = [x for x in info if len(x) != 0]
				f.write('|'.join(info) + '\n')
				l.info(info)
			page += 1
			

	except Exception as e:
		l.error(str(e))


if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception as e:
		l.critical(str(e))
	finally:
		f.close()
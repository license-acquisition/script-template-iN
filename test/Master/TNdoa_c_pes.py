import csv, codecs, requests, time #optional: re, string
from bs4 import BeautifulSoup
from script_template import create_file, logger

#Always use canonical headers
f = create_file('pes_c_TNdoa', 'w', [21,12,0,1,"ctiy,state,zip",])
l = logger('TNdoa')	

def main():
	start = 0 #change start and end
	end = 500 #5000
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
                        l.info("|".join(info) + "\n")
                except Exception, e:
                        l.error(str(e))
                        continue
			
if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception, e:
		l.critical(str(e))
	finally:
		f.close()

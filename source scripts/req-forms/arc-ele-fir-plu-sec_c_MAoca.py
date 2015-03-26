import sys, time, re, requests, codecs, logging
from bs4 import BeautifulSoup as soupify
from thready import threaded
from script_template import create_file, logger
logging.basicConfig()

f = create_file('arc-ele-fir-plu-sec_c_MAoca', 'w', ['35', '7', 'City/State', '32', '21', '37', '13', '19'])
l = logger('arc-ele-fir-plu-sec_c_MAoca')

g = codecs.open('arc-ele-fir-plu-sec_c_MAoca_links.txt', 'w', 'utf-8')

def getCities(license_type):
        alphabet = map(chr, range(65, 91))
        cities = []
        for letter in alphabet:
                l.debug(' - - - - - Retrieving %s cities - - - - - ' %letter)
                soup = soupify(requests.get('http://license.reg.state.ma.us/loca/locaCity.asp?qcity=%s&profession=%s' %(letter, license_type)).content)
                for link in soup.find_all('a'):
                        try:
                                if 'locaRange.asp' in link['href']: cities.append(link.text)
                        except:
                                pass
        l.info('number of cities: %s' %len(cities))
        scrapeLinks(cities, license_type)

def scrapeLinks(cities, license_type):
        for city in cities:
                l.debug(' - - - - - Retrieving links from %s - - - - - ' %city)
                soup = soupify(requests.get('http://license.reg.state.ma.us/loca/locaRange.asp?profession=%s&city=%s' %(license_type, city)).content)
                for link in soup.find_all('a'):
                        try:
                                if 'Detailed Licensee Info' in link['title'] and int(link.text):
                                        g.write(link['href'] + '\n')
                        except:
                                pass

def ThreadedScrape():
        links = [x.strip() for x in codecs.open('arc-ele-fir-plu-sec_c_MAoca_links.txt').readlines()]
        l.info('Number of links: %s' %len(links))
        threaded(links, MAoca, num_threads=3)

def MAoca(link):
        url = 'http://license.reg.state.ma.us' + link.replace('\n','')
        soup = soupify(requests.get(url).content)

        licensee = soup.findAll("caption", {"class" : "licensee"})
        split_licensee = licensee[0].text.split('\n')
        tally = 0
        tank = []
        info = []
        for part in split_licensee:
                if 'Licensee' not in part and 'Name:' not in part and 'New Search' not in part and len(part) != 0:
                        tally += 1
                        tank.append(part)
        if tally == 3:
                for fish in tank:
                        info.append(fish.strip().replace(u'\xa0',u''))
        elif tally == 2:
                info.append(tank[0].strip().replace(u'\xa0',u''))
                info.append('')
                info.append(tank[1].replace(u'\xa0',u''))
        upcases = soup.find_all('td', {'class': 'upcase'})
        for i in range(1, 6):
                info.append(upcases[i].text.strip().replace(u'\xa0',u'').replace(u'\t\r\n\r\n',u' ')) # license_type, license_number, status, expiration_date, first_issue_date
        f.write("|".join(info) + "\n")
        l.info(info)

# Main Code
if __name__ == '__main__':
        license_types = ['Architect', 'Gasfitting_Firms', 'Electrical,_Fire_and_Security_Business', 'Plumbing_Firms']
        try:
                for license_type in license_types:
                        l.debug(' - - - - - Starting scrape of %s Licenses - - - - - ' %license_type)
                        getCities(license_type)
                g.close()
                ThreadedScrape()
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
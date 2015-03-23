'''
Chris Jimenez
2015-02-19
'''
import sys, time, re, requests, codecs, logging
from bs4 import BeautifulSoup as soupify
from thready import threaded
logging.basicConfig()

start = time.time()
f = codecs.open("ele_c_MAoca_%s_000.txt" %(time.strftime('%Y%m%d')),"w", "utf-8")
headers = ['qualifying_individual', 'company_name', 'City/State', 'license_type_cd', 'license_number', 'status', 'expiration_date', 'issue_date']
f.write("|".join(headers) + "\n")

#l = codecs.open('ele_c_MAoca_LINKS2.txt', 'w', 'utf-8')

def getCities(license_type):
        alphabet = map(chr, range(65, 91))
        cities = []
        for letter in alphabet:
                print ' - - - - - Retrieving %s cities - - - - - ' %letter
                soup = soupify(requests.get('http://license.reg.state.ma.us/loca/locaCity.asp?qcity=%s&profession=%s' %(letter, license_type)).content)
                for link in soup.find_all('a'):
                        try:
                                if 'locaRange.asp' in link['href']: cities.append(link.text)
                        except:
                                pass
        print len(cities)
        scrapeLinks(cities, license_type)

def scrapeLinks(cities, license_type):
        for city in cities:
                print ' - - - - - Retrieving links from %s - - - - - ' %city
                soup = soupify(requests.get('http://license.reg.state.ma.us/loca/locaRange.asp?profession=%s&city=%s' %(license_type, city)).content)
                for link in soup.find_all('a'):
                        try:
                                if 'Detailed Licensee Info' in link['title'] and int(link.text):
                                        l.write(link['href'] + '\n')
                        except:
                                pass

def ThreadedScrape():
        links = [x.strip() for x in codecs.open('ele_c_MAoca_LINKS2.txt').readlines()]
        print len(links)
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
        info.append(upcases[1].text.strip().replace(u'\xa0',u'').replace(u'\t\r\n\r\n',u' ')) # license type
        info.append(upcases[2].text.strip().replace(u'\xa0',u'')) # license number
        info.append(upcases[3].text.strip().replace(u'\xa0',u'')) # status
        info.append(upcases[4].text.strip().replace(u'\xa0',u'')) # expiration date
        info.append(upcases[5].text.strip().replace(u'\xa0',u'')) # issue_date
        f.write("|".join(info) + "\n")
        print info

# Main Code
license_types = ['Architect'] # original = ['Gasfitting_Firms', 'Electrical,_Fire_and_Security_Business', 'Plumbing_Firms']
#for license_type in license_types:
        #print ' - - - - - Starting scrape of %s Licenses - - - - - ' %license_type
        #getCities(license_type)
#l.close()
ThreadedScrape()
f.write('Minutes elapsed: %s \n' %((time.time() - start)/60))
f.write('It actually finished.')
f.close()

from bs4 import BeautifulSoup as soupify
from selenium import webdriver
import re, time, codecs, sys

start = time.time()
#browser = webdriver.PhantomJS()
browser = webdriver.Chrome()
f = codecs.open('plu_c_DCitb_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['license_number', 'entity_name', 'city', 'state', 'zip', 'issue_date', 'expiration_date', 'status', 'LicenseOrigin', 'licensee_type_cd']
f.write('|'.join(headers) + '\n')

# two letter search had 500+ results
alphabet = map(chr, range(97, 123))
#browser.get("https://www.asisvcs.com/services/licensing/DCOPLA/search_page.asp?CPCAT=4909STATEREG")
for letter1 in alphabet[23:]: # original: no subsets!
    for letter2 in alphabet[1:]:
        for letter3 in alphabet:
            browser.get("https://www.asisvcs.com/services/licensing/DCOPLA/search_page.asp?CPCAT=4909STATEREG")
            print ' - - - - - Searching %s%s%s - - - - - ' %(letter1.upper(), letter2.upper(), letter3.upper())
            browser.find_element_by_xpath('//*[@id="mainContent"]/form/table/tbody/tr[1]/td[2]/input[2]').click()
            browser.find_element_by_xpath('//*[@id="mainContent"]/form/table/tbody/tr[3]/td[3]/input').send_keys(letter1+letter2+letter3)
            browser.find_element_by_name("submit1").click()
            try:
                soup = soupify(browser.page_source)
                for tr in soup.find_all('table', {'id': 'results'})[0].find_all('tr')[2:]:
                    info = []
                    count = 0
                    for td in tr.find_all('td'):
                        if count == 3:
                            info.append(re.search(r'[0-9]{2}-[A-Za-z]{3}-[0-9]{4}', td.text).group()) # issue
                            info.append(re.search(r'[0-9]{2}-[A-Za-z]{3}-[0-9]{4}', td.text[1:]).group()) # expiration
                        elif count == 2: #address
                            info.append(td.text.split(',')[0].strip()) # city
                            info.append(td.text.split(',')[1].strip()[:2]) # state
                            info.append(td.text.split(',')[1].strip()[2:].strip()) # zip
                        else:
                            info.append(td.text.strip())
                        count += 1
                    print info
                    f.write('|'.join(info) + '\n')
                time.sleep(1)
                browser.back()
            except Exception, e:
                print str(e)
                print 'Failed on %s%s%s' %(letter1.upper(), letter2.upper(), letter3.upper())
                time.sleep(1)
                browser.back()

f.write('Minuts elapsed: %s \n' %((time.time() - start)/60.0))
f.write('It actually finished.')
f.close()

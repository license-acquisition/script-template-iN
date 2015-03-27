from bs4 import BeautifulSoup as soupify
from selenium import webdriver
import re, time, codecs, sys
from itertools import product
from string import ascii_lowercase
from script_template import create_file, logger

f = create_file('plu_c_DCitb', 'w', ['21', '12', '4', '36', '44', '19', '13', '37', 'LicenseOrigin', '32'])
l = logger('plu_c_DCitb')

driver = webdriver.PhantomJS()
for keyword in [''.join(i) for i in product(ascii_lowercase, repeat =3)]:
    driver.get("https://www.asisvcs.com/services/licensing/DCOPLA/search_page.asp?CPCAT=4909STATEREG")
    l.info(' - - - - - Searching %s - - - - - ' %(keyword))
    driver.find_element_by_xpath('//*[@id="mainContent"]/form/table/tbody/tr[1]/td[2]/input[2]').click()
    driver.find_element_by_xpath('//*[@id="mainContent"]/form/table/tbody/tr[3]/td[3]/input').send_keys(keyword)
    driver.find_element_by_name("submit1").click()
    try:
        soup = soupify(driver.page_source)
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
            l.info(info)
            f.write('|'.join(info) + '\n')
    except Exception, e:
        l.error(str(e))
        l.error('Failed on %s' %(keyword))
    time.sleep(1)
    driver.back()

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
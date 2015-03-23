from selenium import webdriver
from bs4 import BeautifulSoup
import re, time, codecs

f = codecs.open("arc_b_IAiwd_%s_000.txt" %(time.strftime('%Y%m%d')),"w","utf-8")
headers = ['name', 'blank', 'entity_name', 'address1', 'address2', 'city/state/zip', 'phone', 'fax', 'license_number',
           'blank', 'licensee_type_cd', 'status', 'expiration_date', 'issue_date', 'method']
f.write('|'.join(headers) + '\n')
start = time.time()
browser = webdriver.Chrome()
for i in range(1,30000):
    try:
        info = ''
        browser.get("https://eservices.iowa.gov/licensediniowa/index.php?pgname=pubsearch")
        time.sleep(1)
        pro = browser.find_element_by_name("profession_lic")
        pro.send_keys("E")
        time.sleep(1)
        search = browser.find_element_by_css_selector("body > form > table > tbody > tr > td > table > tbody > tr:nth-child(5) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > input[type='text']")
        search.send_keys("%05d"%i)
        browser.find_element_by_css_selector("body > form > table > tbody > tr > td > table > tbody > tr:nth-child(5) > td > table > tbody > tr:nth-child(3) > td > div > input[type='submit']:nth-child(2)").click()
        browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(2) > td > a").click()
        # get soup for page
        soup = BeautifulSoup(browser.page_source)
        info += soup.find('font', {'size': '+1'}).text.replace('\n','').strip() + '|'
        for td in soup.find_all('td', {'colspan': '1', 'nowrap': 'nowrap'}):
            try:
                if len(td.text.split(':')) > 2:
                    info += td.text.split(':')[3].replace('\n','').replace('\r','').strip() + '|'
                else:
                    info += td.text.split(':')[1].replace('\n','').replace('\r','').strip() + '|'
            except:
                info += td.text.replace('\n','').replace('\r','').strip() + '|'
        '''
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(2) > td > font > strong").text) # qualifying individual
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(1) > td").text) # entity_name
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(2) > td").text) # address1
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(3) > td").text) # address2
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(4) > td:nth-child(1) > table > tbody > tr:nth-child(3) > td").text) # city/state/zip
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(6) > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(1) > td:nth-child(2) > pre").text)
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(6) > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(2) > td:nth-child(2) > pre").text)
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(6) > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(3) > td:nth-child(2) > pre").text)
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(6) > td:nth-child(2) > table > tbody > tr > td:nth-child(1) > table > tbody > tr:nth-child(4) > td:nth-child(2)").text)
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(6) > td:nth-child(2) > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(1) > td:nth-child(2) > pre").text)
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(6) > td:nth-child(2) > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(2) > td:nth-child(2)").text)
        info.append(browser.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(6) > td:nth-child(2) > table > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(3) > td:nth-child(2)").text)
        '''
        print info
        f.write(info + '\n')
    except Exception, e:
    	print "Nothing found on %d"%i
    	#print str(e)

end = time.time()
final = (end-start)/60
f.write('It actually finished \n')
f.write('Minutes: ' + str(final))

f.close()
browser.quit()

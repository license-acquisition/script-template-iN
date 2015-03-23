from bs4 import BeautifulSoup
from selenium import webdriver
import mechanize, urllib2, requests, re, cookielib, time, codecs

start = time.time()
s = requests.Session()
s.get('https://mylicense.in.gov/everification/Search.aspx?facility=Y')
driver = webdriver.Chrome() #instantiate a webdriver
cj = cookielib.LWPCookieJar() #cookie jar

count = []

f=codecs.open("plu_c_INoli_%s_000.txt" %(time.strftime('%Y%m%d')),"w", "utf-8")
headers = ['entity_name', 'city/state/zip', 'license_number', 'authority', 'licensee_type_cd', 'Method', 'issue_date', 'expiration_date', 'status']
f.write('|'.join(headers) + '\n')

alphabet = map(chr, range(65,91))
for letter in alphabet:
    tally = 0
    driver.get("https://mylicense.in.gov/everification/Search.aspx?facility=Y") #open the url
    driver.find_element_by_xpath('//*[@id="t_web_lookup__profession_name"]/option[39]').click()
    driver.find_element_by_xpath('//*[@id="t_web_lookup__full_name"]').send_keys(letter)    
    driver.find_element_by_xpath('//*[@id="sch_button"]').click()
    
    for i in range(2, 15):
        print ' - - - - - Page %s - - - - - ' %(i-1)
        soup = BeautifulSoup(driver.page_source)
        trs = [x for x in soup.find_all('a') if 'Details.aspx' in x['href']]
        for tr in trs:
            # get soup
            url = 'https://mylicense.in.gov/everification/'
            driver.get(url + tr['href'])
            soup2 = BeautifulSoup(driver.page_source)
    
            info = []
            data = soup2.find_all('span', {'class': 'label'})
            for dt in data:
                info.append(dt.text.strip())
        
            # write payload to file
            f.write("|".join(info) + "\n")
            tally += 1
            # print to console for QA
            print info

            # make sure it goes back to search results every time
            driver.back()
            time.sleep(1)
            if 'Search Results' in driver.page_source:
                pass
            else:
                driver.back()
        if i == 14: break    
        # quit and move browser to next page
        time.sleep(2)
        try:
            driver.find_element_by_link_text(str(i)).click()
            print ' - - - - - Clicking to page %s - - - - - ' %i
        except:
            print ' - - - - - Done with %s - - - - - ' %letter
            count.append({letter: tally})
            break

final = (time.time()-start)/60
f.write('Minutes elapsed: %s' %(str(final)))
f.close()

from bs4 import BeautifulSoup
from selenium import webdriver
import mechanize, urllib2, requests, re, cookielib, time, codecs


start = time.time()
s = requests.Session()
s.get('https://mylicense.in.gov/everification/Search.aspx?facility=Y')

count=0

f=codecs.open("arc_eng_b_INoli_%s_000.txt" %(time.strftime('%Y%m%d')),"w", "utf-8")
headers = ['entity_name', 'city/state/zip', 'license_number', 'authority', 'licensee_type_cd', 'Method', 'issue_date', 'expiration_date', 'status']
f.write('|'.join(headers) + '\n')
driver = webdriver.Chrome() #instantiate a webdriver
cj = cookielib.LWPCookieJar() #cookie jar

license_types = [[6, 1], [7,2], [17, 1], [24, 3], [24, 4], [26,2]]
alphabet = map(chr, range(65,91))
for license_type in license_types:
    for letter in alphabet:
        driver.get("https://mylicense.in.gov/everification/Search.aspx?facility=Y") #open the url
        driver.find_element_by_xpath('//*[@id="t_web_lookup__profession_name"]/option[%s]' %(license_type[0])).click()
        driver.find_element_by_xpath('//*[@id="t_web_lookup__license_type_name"]/option[%s]' %(license_type[1])).click()
        driver.find_element_by_xpath('//*[@id="t_web_lookup__full_name"]').send_keys(letter)
        driver.find_element_by_xpath('//*[@id="sch_button"]').click()
        url = 'https://mylicense.in.gov/everification/'
        print ' - - - - - Searching %s - - - - - ' %letter
        for i in range(2, 20):
            print ' - - - - - Page %s - - - - - ' %(i-1)
            try:
                soup = BeautifulSoup(driver.page_source)
                trs = [x for x in soup.find_all('a') if 'Details.aspx' in x['href']]
                for tr in trs:
                    driver.get(url + tr['href'])
                    soup2 = BeautifulSoup(driver.page_source)
                         
                    info = []
                    for dt in soup2.find_all('span', {'class': 'label'}):
                        info.append(dt.text.strip())
                
                    # write payload to file
                    f.write("|".join(info) + "\n")
                    print info
                    
                    # make sure it goes back to search results every time
                    driver.back()
                    time.sleep(1)
                    if 'Search Results' in driver.page_source:
                        pass
                    else:
                        driver.back()
                    
            except:
                print 'Page had no results.'  
            # quit and move browser to next page
            try:
                driver.find_element_by_link_text(str(i)).click()
            except:
                break

final = (time.time()-start)/60
f.write('Minutes elapsed: %s' %(str(final)))
f.close()

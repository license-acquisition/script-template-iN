from bs4 import BeautifulSoup
from selenium import webdriver
import mechanize, urllib2, requests, re, cookielib, time, codecs
from script_template import create_file, logger

f = create_file('arc-asb-eng-hom-id-lar-led-oth-sur_c_INoli', 'w', ['12', 'city/state/zip', '21', 'authority', '32', 'Method', '19', '13', '37'])
l = logger('arc-asb-eng-hom-id-lar-led-oth-sur_c_INoli')

s = requests.Session()
s.get('https://mylicense.in.gov/everification/Search.aspx?facility=Y')
driver = webdriver.PhantomJS() #instantiate a webdriver

def main():
    count=0
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
            l.debug(' - - - - - Searching %s - - - - - ' %letter)
            for i in range(2, 20):
                l.debug(' - - - - - Page %s - - - - - ' %(i-1))
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
                    l.error('Page had no results.')
                # quit and move browser to next page
                try:
                    driver.find_element_by_link_text(str(i)).click()
                except:
                    break

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()

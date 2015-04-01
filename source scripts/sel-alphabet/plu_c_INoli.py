from bs4 import BeautifulSoup
from selenium import webdriver
import urllib2, requests, re, cookielib, time, codecs
from script_template import create_file, logger

f = create_file('plu_c_INoli', 'w', ['12', 'city/state/zip', '21', 'authority', '32', 'Method', '19', '13', '37'])
l = logger('plu_c_INoli')
s = requests.Session()
driver = webdriver.PhantomJS() #instantiate a webdriver

def main():
    s.get('https://mylicense.in.gov/everification/Search.aspx?facility=Y')
    cj = cookielib.LWPCookieJar() #cookie jar
    count = []
    for letter in map(chr, range(65,91)):
        tally = 0
        driver.get("https://mylicense.in.gov/everification/Search.aspx?facility=Y") #open the url
        driver.find_element_by_xpath('//*[@id="t_web_lookup__profession_name"]/option[39]').click()
        driver.find_element_by_xpath('//*[@id="t_web_lookup__full_name"]').send_keys(letter)    
        driver.find_element_by_xpath('//*[@id="sch_button"]').click()
        
        for i in range(2, 15):
            l.debug(' - - - - - Page %s - - - - - ' %(i-1))
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
                l.info(info)

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
                l.debug(' - - - - - Clicking to page %s - - - - - ' %i)
            except:
                l.debug(' - - - - - Done with %s - - - - - ' %letter)
                count.append({letter: tally})
                break

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
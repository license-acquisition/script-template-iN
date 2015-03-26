from selenium import webdriver
from bs4 import BeautifulSoup
import re, time, codecs
from script_template import create_file, logger

f = create_file('arc_b_IAiwd', 'w', ['name', 'blank', '12', '0', '1', 'city/state/zip', '33', '66', '21', 'blank', '32', '37', '13', '19', 'method'])
l = logger('arc_b_IAiwd')
driver = webdriver.PhantomJS()

def main():
    for i in range(1,30000):
        try:
            info = ''
            driver.get("https://eservices.iowa.gov/licensediniowa/index.php?pgname=pubsearch")
            time.sleep(1)
            pro = driver.find_element_by_name("profession_lic")
            pro.send_keys("E")
            time.sleep(1)
            search = driver.find_element_by_css_selector("body > form > table > tbody > tr > td > table > tbody > tr:nth-child(5) > td > table > tbody > tr:nth-child(1) > td:nth-child(2) > div > input[type='text']")
            search.send_keys("%05d"%i)
            driver.find_element_by_css_selector("body > form > table > tbody > tr > td > table > tbody > tr:nth-child(5) > td > table > tbody > tr:nth-child(3) > td > div > input[type='submit']:nth-child(2)").click()
            driver.find_element_by_css_selector("body > form > table > tbody > tr:nth-child(2) > td > a").click()
            # get soup for page
            soup = BeautifulSoup(driver.page_source)
            info += soup.find('font', {'size': '+1'}).text.replace('\n','').strip() + '|'
            for td in soup.find_all('td', {'colspan': '1', 'nowrap': 'nowrap'}):
                try:
                    if len(td.text.split(':')) > 2:
                        info += td.text.split(':')[3].replace('\n','').replace('\r','').strip() + '|'
                    else:
                        info += td.text.split(':')[1].replace('\n','').replace('\r','').strip() + '|'
                except:
                    info += td.text.replace('\n','').replace('\r','').strip() + '|'
            l.info(info)
            f.write(info + '\n')
        except Exception, e:
        	l.info("Nothing found on %d"%i)
            l.error(str(e))

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()

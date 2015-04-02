from bs4 import BeautifulSoup
import urllib, requests, codecs, re, sys, time
from selenium import webdriver
from glob import glob
from script_template import create_file, logger

f = create_file('gen_res_c_ALlbg', 'w', ['12', '21', '0', '4', '36', '44', '33', '13'])
l = logger('gen_res_c_ALlbg')
driver = webdriver.PhantomJS()


def main():
    url = 'http://genconbd.alabama.gov/DATABASE-SQL/roster.aspx'
    short_url = 'http://genconbd.alabama.gov/DATABASE-SQL/'

    count = 1
    winners = 0
    page = 1

    #driver = webdriver.PhantomJS(glob('C:\\Users\\*\\Downloads\\phantomjs.exe'))
    driver.get(url)

    # iterate through list
    while page < 605:
        l.debug(page)
        soup = BeautifulSoup(driver.page_source)
        table = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_GridView1'})
        links = []
        for link in table.find_all('a'):
            if 'detail' in link['href']:
                detail_url = short_url + link['href']
                stew = BeautifulSoup(requests.get(detail_url).content)
                try:
                    info = []
                    info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_NameLabel"}).text.strip()) #nameprint
                    info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_LicenseNoLabel"}).text.strip()) #licno
                    info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_AddressLabel"}).text.strip()) #address
                    info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_CityLabel"}).text.strip()) #city
                    info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_StateLabel"}).text.strip()) #state
                    info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_ZipLabel"}).text.strip()) #zipcode
                    info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_PhonenoLabel"}).text.strip()) #phone
                    info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_Expr1Label"}).text.strip()) #expdate
                    l.info(info)
                    f.write('|'.join(info) + '\n')
                    winners += 1
                except Exception as e:
                    #print 'Roll Tide bitch'
                    l.error(str(e))
                    count += 1
                    if count%100==0:
                        l.error('We\'ve failed quite a bit.')
                        l.error('Winners: ' + str(winners))
                        l.error('Count: ' + str(count))
        page+=1
        try:                   
            driver.find_element_by_link_text(str(page)).click()
        except:
            if page == 11:
                driver.find_elements_by_link_text('...')[0].click()
            else:
                driver.find_elements_by_link_text('...')[1].click()

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
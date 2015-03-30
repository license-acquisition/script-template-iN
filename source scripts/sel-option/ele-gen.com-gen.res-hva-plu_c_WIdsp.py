# Hassan Uraizee WI script 

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException 
import csv
import codecs, time
from script_template import create_file, logger

f = create_file('ele-gen.com-gen.res-hva-plu_c_WIdsp', 'w', ['21', '12', 'First/Middle Name', '0', 'License Name'])
l = logger('ele-gen.com-gen.res-hva-plu_c_WIdsp')
driver = webdriver.PhantomJS()

def main():
    url = 'https://app.wi.gov/licensesearch'
    driver.get(url)
    #driver.find_element_by_css_selector(".accordion > dd:nth-child(4) > a:nth-child(1)")

    soup = BeautifulSoup(driver.page_source)
    select = soup.find('select',{'id': "CredentialViewModel_CredentialType_CredNameCode"})
    option_tags = select.find_all('option')
    option_tags = option_tags[1:]
    info = []
    name = driver.find_element_by_id('tadvancedzip')
    true = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div/dl/dd[4]/a')
    true.click()
    select = driver.find_element_by_xpath('//*[@id="CredentialStatusCode"]/option[2]')
    select.click()
    search = driver.find_element_by_xpath('//*[@id="TradeCredAdvSearch"]')

    def check_exists_by_xpath(xpath):
        try:
             soupo = BeautifulSoup(driver.page_source)
             driver.find_element_by_xpath(xpath)
             info = []
             table1 = soupo.find_all('td')
             counter = 1
             for i in table1:
                 info.append(i.text)
                 counter += 1
                 if counter % 6 == 0: 
                      f.write('|'.join(info) + '\n')
                      info = []
                      counter = 1            

        except NoSuchElementException:
            return False
        return True

    companyType = ['21','23','24','25','29','37','53','54','61','82']
    for i in range(len(companyType)):
        l.debug(companyType[i])
        a = driver.find_element_by_xpath('//*[@id="CredentialViewModel_CredentialType_CredNameCode"]/option['+companyType[i]+']')
        a.click()
        for x in range(0,9):
            name.clear()
            name.send_keys(x)
            search.click()
            check_exists_by_xpath('/html/body/div[3]/div[3]/div/table/thead/tr/th[1]')
            driver.get(url)
            name = driver.find_element_by_id('tadvancedzip')
            true = driver.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div/dl/dd[4]/a')
            true.click()
            select = driver.find_element_by_xpath('//*[@id="CredentialStatusCode"]/option[2]')
            select.click()
            a = driver.find_element_by_xpath('//*[@id="CredentialViewModel_CredentialType_CredNameCode"]/option['+companyType[i]+']')
            a.click()
            search = driver.find_element_by_xpath('//*[@id="TradeCredAdvSearch"]')


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
# Hassan Uraizee WI script 

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException 
import csv
import codecs, time
h = codecs.open('ele-gen.com-gen.res-hva-plu_c_WIdsp_%s_000.csv'%(time.strftime('%Y%m%d')),'w','UTF-8')
f = csv.writer(h, delimiter =',',quotechar =' ',quoting=csv.QUOTE_MINIMAL)

browser = webdriver.Chrome()
url = 'https://app.wi.gov/licensesearch'
browser.get(url)
browser.find_element_by_css_selector(".accordion > dd:nth-child(4) > a:nth-child(1)")

soup = BeautifulSoup(browser.page_source)
select = soup.find('select',{'name': "CredentialViewModel.CredentialType.CredNameCode"})
option_tags = select.findAll('option')
option_tags = option_tags[1:]
info = []
name = browser.find_element_by_id('tadvancedzip')
true = browser.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div/dl/dd[4]/a')
true.click()
select = browser.find_element_by_xpath('//*[@id="CredentialStatusCode"]/option[2]')
select.click()
search = browser.find_element_by_xpath('//*[@id="TradeCredAdvSearch"]')
#title = ['Name: ', 'Hassan Uraiee', 'State: ', 'Wisconsin', 'URL: ', 'https://app.wi.gov/licensesearch']
data =  ['license_number', 'entity_name', 'First/Middle Name', 'address1', 'License Name']
print data
#f.writerow(title)
f.writerow(data)
def check_exists_by_xpath(xpath):
    try:
         soupo = BeautifulSoup(browser.page_source)
         browser.find_element_by_xpath(xpath)
         info = []
         table1 = soupo.find_all('td')
         counter = 1
         for i in table1:
             info.append(i.text)
             counter += 1
             if counter % 6 == 0: 
                  f.writerow(info)
                  info = []
                  counter = 1            

    except NoSuchElementException:
        return False
    return True

companyType = ['21','23','24','25','29','37','53','54','61','82']
for i in range(len(companyType)):
    print companyType[i]
    a = browser.find_element_by_xpath('//*[@id="CredentialViewModel_CredentialType_CredNameCode"]/option['+companyType[i]+']')
    a.click()
    for x in range(0,9):
        name.clear()
        name.send_keys(x)
        search.click()
        check_exists_by_xpath('/html/body/div[3]/div[3]/div/table/thead/tr/th[1]')
        browser.get(url)
        name = browser.find_element_by_id('tadvancedzip')
        true = browser.find_element_by_xpath('//*[@id="wrapper"]/div[2]/div/dl/dd[4]/a')
        true.click()
        select = browser.find_element_by_xpath('//*[@id="CredentialStatusCode"]/option[2]')
        select.click()
        a = browser.find_element_by_xpath('//*[@id="CredentialViewModel_CredentialType_CredNameCode"]/option['+companyType[i]+']')
        a.click()
        search = browser.find_element_by_xpath('//*[@id="TradeCredAdvSearch"]')

browser.close()
browser.quit()
h.close()
f.close()

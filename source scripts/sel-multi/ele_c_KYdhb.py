import sys, requests, time, re, csv, codecs
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import selenium.webdriver.support.ui as UI
from script_template import create_file, logger

f = create_file('ele_c_KYdhb', 'w', ['21', '12', '13', '32', '37', '4', '8', '36', '6'])
l = logger('ele_c_KYdhb')
driver = webdriver.PhantomJS()

def main():
        driver.implicitly_wait(1)
        driver.get('http://dhbc.ky.gov/bce/ei/el/Pages/default.aspx')
        driver.get('https://ky.joportal.com/License/Search')
        Select(driver.find_element_by_id("Division")).select_by_visible_text("Electrical Licensing")
        #changetohvachere
        driver.implicitly_wait(1)
        driver.find_element_by_xpath("//button[@type='button']").click()
        driver.implicitly_wait(1)
        driver.find_element_by_css_selector("#ui-multiselect-LicenseType-option-0").click()
        driver.implicitly_wait(1)
        driver.find_element_by_id("btnSubmit").click()
        time.sleep(3)
        #driver.find_element_by_css_selector("input.ui-pg-input").clear()
        #driver.find_element_by_css_selector("input.ui-pg-input").send_keys("1092").send_keys("Keys.ENTER")
        keys = driver.find_element_by_xpath("//*[@id='licenseSearchGridPagingBar_center']/table/tbody/tr/td[8]/select")
        keys.send_keys('50' + 'Keys.RETURN') #grab 50 results per page
        #elem = driver.find_element_by_css_selector("input.ui-pg-input")
        #elem.clear
        #elem.send_keys('1092' + 'Keys.RETURN')
        time.sleep(1)
        count = 1
        #driver.send_keys("Keys.ENTER")
        #driver.find_element_by_css_selector("span.ui-icon.ui-icon-seek-next").send_keys("Keys.ENTER")
        while count < 7:
                l.debug(' - - - - - - %s of 400 - - - - - - ' %count)
                time.sleep(5)
                #driver.wait_element_to_be_present
                c = driver.page_source
                soup = BeautifulSoup(c)
                matt = soup.findAll("tbody")[3]
                trs = soup.findAll("tbody")[3]
                for tr in trs:
                        info = []
                        tds = tr.findAll("td")
                        try:
                                info.append(tds[2].text) # licnum
                                info.append(tds[3].text) # name
                                info.append(tds[4].text) # expdate
                                info.append(tds[5].text) # typecd
                                info.append(tds[6].text) # status
                                info.append(tds[7].text) # city
                                for td in tds[8].text.split(','):
                                        info.append(td.strip()) # county and state
                                info.append('1') # company flag
                                l.info(info)
                                f.write('|'.join(info) + '\n')
                        except:
                                continue
                time.sleep(5)
                driver.find_element_by_css_selector("span.ui-icon.ui-icon-seek-next").click()
                time.sleep(5)
                count += 1


if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception, e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()
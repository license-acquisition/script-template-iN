from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from script_template import create_file, logger
import codecs, re, csv, time

def main():
        
        # create file and logger
        f = create_file('eng-sur_c_MSbes', 'w', [7, 'address, city, state, zip', 8, 33, 32, 21, 13, 35])
        l = logger('MSbes')
        l.info('Starting - - - - ')
        # initialize webdriver
        driver = webdriver.PhantomJS()
        driver.get("https://www.peps.apps.its.ms.gov/PublicView/PublicCompanySearch.aspx")
        driver.find_element_by_css_selector("input[value=Search]").click()

        j = 2
        while j < 49:
                try:
                        for i in range(0, 50):
                                print i
                                fail = 0
                                while fail == 0:
                                        try:    
                                                driver.find_elements_by_partial_link_text("Select")[i].click()
                                                fail = 1
                                        except Exception as e:
                                                l.error(str(e))
                        
                                try:
                                        # wait for element to appear, then soupify page
                                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"ctl00_Main_btnBack")))
                                        soup = BeautifulSoup(driver.page_source)       

                                        parse(soup) # parse function
                                        
                                except Exception as e:
                                        l.error(str(e))

                                driver.back() #find_element_by_id("ctl00_Main_btnBack").click()
                        
                        # navigate to next page
                        if j == 11:
                                driver.find_elements_by_partial_link_text("...")[0].click()
                        elif j % 10 == 1:
                                driver.find_elements_by_partial_link_text("...")[1].click()
                        else:   
                                driver.find_element_by_partial_link_text(str(j)).click()
                        j = j + 1
                except Exception, e:
                        l.error(str(e))
        f.close()
        driver.quit()

def parse(soup):
        info = []
                
        info.append(soup.find_all("span", {"class" : "cssText"})[0].next)
        info.append(soup.find_all("span", {"class" : "cssText"})[1].next)
        info.append(soup.find_all("span", {"class" : "cssText"})[2].next)
        info.append(soup.find_all("span", {"class" : "cssText"})[3].next)
        info.append(soup.find_all("span", {"class" : "cssText"})[4].next)
        info.append(soup.find_all("span", {"class" : "cssText"})[5].next)
        info.append(soup.find_all("span", {"class" : "cssText"})[6].next)
        info.append(soup.find_all("span", {"class" : "cssText"})[7].next)

        f.write('|'.join(info) + '\n')
        l.info(info)

if __name__ == '__main__':
        main()

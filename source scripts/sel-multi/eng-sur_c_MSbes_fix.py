from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs, re, csv, time
from script_template import create_file, logger

f = create_file('eng-sur_c_MSbes', 'w', ['headers'])
l = logger('eng-sur_c_MSbes')
browser = webdriver.PhantomJS()

def main():
        browser.get("https://www.peps.apps.its.ms.gov/PublicView/PublicCompanySearch.aspx")
        browser.find_element_by_css_selector("input[value=Search]").click()
        j = 2
        while j < 49:
                try:
                        for i in range(0, 50):
                                print i
                                fail = 0
                                while fail == 0:
                                        try:    
                                                browser.find_elements_by_partial_link_text("Select")[i].click()
                                                fail = 1
                                        except Exception as e:
                                    
                                                l.error('Level 1: '+str(e))
                        
                                try:
                                        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID,"ctl00_Main_btnBack")))
                                        soup = BeautifulSoup(browser.page_source)       
                
                                        info = []
                
                                        info.append(soup.find_all("span", {"class" : "cssText"})[0].next)
                                        info.append(soup.find_all("span", {"class" : "cssText"})[1].next)
                                        info.append(soup.find_all("span", {"class" : "cssText"})[2].next)
                                        info.append(soup.find_all("span", {"class" : "cssText"})[3].next)
                                        info.append(soup.find_all("span", {"class" : "cssText"})[4].next)
                                        info.append(soup.find_all("span", {"class" : "cssText"})[5].next)
                                        info.append(soup.find_all("span", {"class" : "cssText"})[6].next)
                                        info.append(soup.find_all("span", {"class" : "cssText"})[7].next)
                        
                                        f.write("|".join(info) + "\n")
                                        l.info(info)
                                except Exception as e:
                            
                                        l.error('Level 2: '+str(e))

                                browser.back()#find_element_by_id("ctl00_Main_btnBack").click()
                        
                        
                        if j == 11:
                                browser.find_elements_by_partial_link_text("...")[0].click()
                        elif j % 10 == 1:
                                browser.find_elements_by_partial_link_text("...")[1].click()
                        else:   
                                browser.find_element_by_partial_link_text(str(j)).click()
                        j = j + 1
                except Exception, e:
                        l.error('Level 3: ' +str(e))

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception, e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()
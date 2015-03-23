from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import codecs, re, csv, time

f = codecs.open('eng-sur_c_MSbes_%s_000.csv'%(time.strftime("%Y%m%d")), 'w', 'utf-8')
browser = webdriver.PhantomJS()
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
                            
                                        print str(e)
                
                        try:
                                WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID,"ctl00_Main_btnBack")))
                                soup = BeautifulSoup(browser.page_source)       
        
                                data = []
        
                                data.append(soup.find_all("span", {"class" : "cssText"})[0].next)
                                data.append(soup.find_all("span", {"class" : "cssText"})[1].next)
                                data.append(soup.find_all("span", {"class" : "cssText"})[2].next)
                                data.append(soup.find_all("span", {"class" : "cssText"})[3].next)
                                data.append(soup.find_all("span", {"class" : "cssText"})[4].next)
                                data.append(soup.find_all("span", {"class" : "cssText"})[5].next)
                                data.append(soup.find_all("span", {"class" : "cssText"})[6].next)
                                data.append(soup.find_all("span", {"class" : "cssText"})[7].next)
                
                                f.write('\"' + "\",\"".join(data) + "\"\n")
                                print ('\"' + '\"\n\"'.join(data))
                        except Exception as e:
                    
                                print str(e)

                        browser.back()#find_element_by_id("ctl00_Main_btnBack").click()
                
                
                if j == 11:
                        browser.find_elements_by_partial_link_text("...")[0].click()
                elif j % 10 == 1:
                        browser.find_elements_by_partial_link_text("...")[1].click()
                else:   
                        browser.find_element_by_partial_link_text(str(j)).click()
                j = j + 1
        except Exception, e:
                print str(e)

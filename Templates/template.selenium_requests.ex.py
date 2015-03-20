###################################
# Output: arc-eng-lar-sur_c_KSbtp
# Method: selenium + requests
###################################

from selenium import webdriver
import requests, re, codecs, time
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('arc-eng-lar-sur_c_KSbtp','w',[12,4,36,21,32,37,19,"renewal_date",13,"obtained_by"])
l = logger('KSbtp')
u = codecs.open('KSbtp.links.csv', 'w',' utf-8')
driver = webdriver.PhantomJS()
s = requests.Session()
s.get("http://licensing.ks.gov/verification/web/Search.aspx?facility=Y")
 
def get_page(n):
        driver.get("http://licensing.ks.gov/verification/web/Search.aspx?facility=Y")
        licenseTypes = [2, 3, 4, 6] # arc, lar, eng, sur
        driver.find_element_by_xpath("//*[@id=\"t_web_lookup__profession_name\"]/option[%s]" %(licenseTypes[n])).click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id=\"sch_button\"]").click()
        time.sleep(3)
        l.debug('- - - - - - Getting License Type %s - - - - - -' %(n+1))
                
def grab_links():
        for link in BeautifulSoup(driver.page_source).find_all("a"):
                if "agency_id" in link['href']:
                                l.info(link.text)
                                u.write(link['href'] + "\n") 
                else:
                        pass

def scrape_links(n):
        i=1
        while True:
                try:
                        l.debug("Grabbing links for", i)
                        grab_links()
                        i+=1
                        driver.find_element_by_link_text("%d"%i).click()
                        time.sleep(3)
                        l.debug("Clicked on", i)
                        time.sleep(3)
                except:
                        if len(driver.find_elements_by_link_text("...")) == 1 and i>41:
                                n += 1
                                if n >= 4: # len(licenseTypes)
                                        break
                                else:
                                        get_page(n)
                                        i = 1
                        elif len(driver.find_elements_by_link_text("...")) == 0:
                                n += 1
                                if n >= 4: # len(licenseTypes)
                                        break
                                else:
                                        get_page(n)
                                        i = 1
                        elif len(driver.find_elements_by_link_text("..."))==1:
                                driver.find_element_by_link_text("...").click()
                        elif len(driver.find_elements_by_link_text("...")) == 2:
                                driver.find_elements_by_link_text("...")[1].click()
        u.close()

def KSbtp(link):
        l.info(link.replace('\n',''))
        try:
                page = s.get("http://licensing.ks.gov/verification/web/" + link.replace('\n',''))
                time.sleep(3)
                soup = BeautifulSoup(re.sub("&amp;", "&", page.content))
                info = []
                info.append("1")
                info.append(soup.find("span", id="_ctl25__ctl1_full_name").text) # entity_name
                info.append(soup.find("span", id="_ctl30__ctl1_addr_city").text) # city
                info.append(soup.find("span", id="_ctl30__ctl1_state").text) # state
                info.append(soup.find("span", id="_ctl30__ctl1_zipcode").text) # zipcode      
                info.append(soup.find("span", id="_ctl35__ctl1_license_no").text) # license_number
                info.append(soup.find("span", id="_ctl35__ctl1_license_type").text) # licensee_type_cd
                info.append(soup.find("span", id="_ctl35__ctl1_status").text) # status
                info.append(soup.find("span", id="_ctl35__ctl1_issue_date").text) # issue_date
                info.append(soup.find("span", id="_ctl35__ctl1_last_ren").text) # renewal_date
                info.append(soup.find("span", id="_ctl35__ctl1_expiry").text) # expiration_date
                info.append(soup.find("span", id="_ctl35__ctl1_obtained_by").text) # obtained_by
                info.append(link.split("=")[-1])
                l.debug(info)
                f.write("|".join(info) + "\n")
        except:
                pass

def get_data():
        for line in open('KSbtp_links.csv', 'r'):
                KSbtp(line)
        
        
# - - - - - MAIN CODE - - - - - 

if __name__ == '__main__':
        try:
                n = 0
                get_page(n)
                scrape_links(n)
                get_data()
                l.info('complete')
        except Exception, e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()
    

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re, codecs, time
from thready import threaded
from script_template import create_file, logger

f = create_file('sec_c_TXdps', 'w', ['6', '7', '21', 'CompanyCode', '32', '0', '4', '36', '44', 'CompanyStatus', 'CompanyExpiration', 'InsuranceExpiration', 'ArmedGuardInsurance', 'GuardDogInsurance'])
l = logger('sec_c_TXdps')
g = codecs.open('sec_c_TXdps_links.csv', 'w', 'utf-8')
driver = webdriver.PhantomJS()
s = requests.Session()
s.get("http://www.txdps.state.tx.us/rsd/psb/psbSearch/company_search.aspx")

def GetPage(n):
        driver.get("http://www.txdps.state.tx.us/rsd/psb/psbSearch/company_search.aspx")
        #time.sleep(3)
        licenseTypes = [2, 10]
        driver.find_element_by_xpath("//*[@id=\"ctl00_SearchContentPlaceHolder_ddType\"]/option[%s]" %(licenseTypes[n])).click()
        #time.sleep(3)
        driver.find_element_by_xpath("//*[@id=\"ctl00_SearchContentPlaceHolder_cmdSearch\"]").click()
        l.debug('- - - - - - - Getting License Type %s - - - - - -' %n)
                
def GrabLinks():
        for link in BeautifulSoup(driver.page_source).findAll("a"):
                if "company_details" in link['href']:
                                l.info(link.text.strip())
                                g.write(link['href'][1:] + "\n") 
                else:
                        pass

def ScrapeLinks(n):
        i=1
        while True:
                try:
                        l.debug("Grabbing links for", i)
                        GrabLinks()
                        i+=1
                        driver.find_element_by_link_text("%d"%i).click()
                        time.sleep(3)
                        l.debug("Clicked on", i)
                        time.sleep(3)
                except:
                        if len(driver.find_elements_by_link_text("...")) == 2 and i>21:
                                n += 1
                                if n >= 2: # len(licenseTypes)
                                        break
                                else:
                                        GetPage(n)
                                        i = 1
                        elif len(driver.find_elements_by_link_text("...")) == 0:
                                n += 1
                                if n >= 2: # len(licenseTypes)
                                        break
                                else:
                                        GetPage(n)
                                        i = 1
                        elif len(driver.find_elements_by_link_text("..."))==2:
                                driver.find_element_by_link_text("...").click()
                        elif len(driver.find_elements_by_link_text("...")) == 4:
                                driver.find_elements_by_link_text("...")[1].click()
                                
        url.close()

def TXdps(link):
        l.info(link.replace('\n',''))
        try:
                page = s.get("http://www.txdps.state.tx.us/rsd/psb/psbSearch" + link.replace('\n',''))
                time.sleep(3)
                soup = BeautifulSoup(page.content.replace('<BR />','_%_').replace('<br />','_%_').replace('<br><br/><BR><BR/>', '_%_'))
                info = []
                info.append("1")
                info.append(soup.find("span", id="ctl00_SearchContentPlaceHolder_lblCompanyName").text) # company_name
                info.append(soup.find("span", id="ctl00_SearchContentPlaceHolder_lblLicNum").text) # license_number
                info.append(soup.find("span", id="ctl00_SearchContentPlaceHolder_lblCode").text) # CompanyCode
                info.append(soup.find("span", id="ctl00_SearchContentPlaceHolder_lblCat").text.replace('_%_','-')[1:]) # licensee_type_cd
                addr = soup.find("span", id="ctl00_SearchContentPlaceHolder_lblMailingAddress").text.split('_%_')
                info.append(addr[0].strip()) # address1
                info.append(addr[1].split(',')[0].strip()) # city
                info.append(addr[1].split(',')[1].strip()[:2]) # state
                info.append(addr[1].split(',')[1].strip()[2:].strip()) # zip
                info.append(soup.find("span", id="ctl00_SearchContentPlaceHolder_lblCompanyStatus").text) # CompanyStatus
                info.append(soup.find("span", id="ctl00_SearchContentPlaceHolder_lblExpirationDate").text) # CompanyExpiration
                info.append(soup.find("span", id="ctl00_SearchContentPlaceHolder_lblInsuranceExpireDate").text) # InsuranceExpiration
                info.append(soup.find("span", id="ctl00_SearchContentPlaceHolder_lblArmedGuard").text) # ArmedGuard
                info.append(soup.find("span", id="ctl00_SearchContentPlaceHolder_lblGuardDog").text) # GuardDog
                info = [x.strip() for x in info]
                l.info(info)
                f.write("|".join(info) + "\n")
        except Exception as e:
                l.error(str(e))

def ThreadedScrape():
        links = []
        for line in codecs.open("sec_c_TXdps.csv","r").readlines():
                links.append(line.strip())
        threaded(links, TXdps, num_threads=1)
        
def main():
        n = 0
        GetPage(n)
        ScrapeLinks(n)
        ThreadedScrape()

# - - - - - MAIN CODE - - - - - 

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()

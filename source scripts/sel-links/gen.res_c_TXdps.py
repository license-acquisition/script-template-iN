from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re, codecs, time
from thready import threaded

start = time.time()
log = codecs.open('TXdps_log.csv','w','utf-8')
#url = open("TXdps_links.csv","w")
f = codecs.open('gen.res_c_TXdps_%s_000.txt'%(time.strftime("%Y%m%d")), 'w', 'utf-8')
f.write("company_flag,company_name,license_number,CompanyCode,licensee_type_cd,address1,city,state,zip,CompanyStatus,CompanyExpiration,InsuranceExpiration,ArmedGuardInsurance,GuardDogInsurance".replace(',','|') + "\n")

browser = webdriver.PhantomJS()
s = requests.Session()
s.get("http://www.txdps.state.tx.us/rsd/psb/psbSearch/company_search.aspx")
 
def GetPage(n):
        browser.get("http://www.txdps.state.tx.us/rsd/psb/psbSearch/company_search.aspx")
        #time.sleep(3)
        licenseTypes = [2, 10]
        browser.find_element_by_xpath("//*[@id=\"ctl00_SearchContentPlaceHolder_ddType\"]/option[%s]" %(licenseTypes[n])).click()
        #time.sleep(3)
        browser.find_element_by_xpath("//*[@id=\"ctl00_SearchContentPlaceHolder_cmdSearch\"]").click()
        print '- - - - - - - Getting License Type %s - - - - - -' %n
                
def GrabLinks():
        for link in BeautifulSoup(browser.page_source).findAll("a"):
                if "company_details" in link['href']:
                                print link.text.strip()
                                url.write(link['href'][1:] + "\n") 
                else:
                        pass

def ScrapeLinks(n):
        i=1
        while True:
                try:
                        print "Grabbing links for", i
                        GrabLinks()
                        i+=1
                        browser.find_element_by_link_text("%d"%i).click()
                        time.sleep(3)
                        print "Clicked on", i
                        time.sleep(3)
                except:
                        if len(browser.find_elements_by_link_text("...")) == 2 and i>21:
                                n += 1
                                if n >= 2: # len(licenseTypes)
                                        break
                                else:
                                        GetPage(n)
                                        i = 1
                        elif len(browser.find_elements_by_link_text("...")) == 0:
                                n += 1
                                if n >= 2: # len(licenseTypes)
                                        break
                                else:
                                        GetPage(n)
                                        i = 1
                        elif len(browser.find_elements_by_link_text("..."))==2:
                                browser.find_element_by_link_text("...").click()
                        elif len(browser.find_elements_by_link_text("...")) == 4:
                                browser.find_elements_by_link_text("...")[1].click()
                                
        url.close()

def TXdps(link):
        print link.replace('\n','')
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
                print info
                f.write("|".join(info) + "\n")
        except:
                if page.status_code != 200:
                        log_list = []
                        log_list.append(url)
                        print page.status_code, url
                        log.write("\"" + "\",\"".join(log_list) + "\"\n")
                        pass

def ThreadedScrape():
        links = []
        for line in codecs.open("TXdps_links.csv","r").readlines():
                links.append(line.strip())
        threaded(links, TXdps, num_threads=1)

def ErrorPass():
        links = []
        for line in codecs.open("TXdps_log.csv","r").readlines():
                links.append(line.strip())
        threaded(links, TXdps, num_threads=1)
        
# - - - - - MAIN CODE - - - - - 

if __name__ == '__main__':
        #n = 0
        #GetPage(n)
        #ScrapeLinks(n)
        ThreadedScrape()
        ErrorPass()

        f.write('It actually finished. \n')
        f.write('Minutes Elapsed: %s' %((time.time() - start)/60))
        f.close()

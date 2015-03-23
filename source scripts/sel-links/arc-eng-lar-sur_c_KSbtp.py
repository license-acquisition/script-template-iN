from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re, codecs, time
from thready import threaded

start = time.time()
log = codecs.open('KSbtp_log.csv','w','utf-8')
#url = open("KSbtp_links.csv","w")
f = codecs.open('arc-eng-lar-sur_c_KSbtp_%s_000.txt'%(time.strftime("%Y%m%d")), 'w', 'utf-8')
f.write("entity_name,city,state,zip,license_number,licensee_type_cd,status,issue_date,renewal_date,expiration_date,ObtainedBy".replace(',','|') + "\n")

browser = webdriver.PhantomJS()
s = requests.Session()
s.get("http://licensing.ks.gov/verification/web/Search.aspx?facility=Y")
 
def GetPage(n):
        browser.get("http://licensing.ks.gov/verification/web/Search.aspx?facility=Y")
        time.sleep(3)
        licenseTypes = [2, 3, 4, 6]
        browser.find_element_by_xpath("//*[@id=\"t_web_lookup__profession_name\"]/option[%s]" %(licenseTypes[n])).click()
        time.sleep(3)
        browser.find_element_by_xpath("//*[@id=\"sch_button\"]").click()
        print '- - - - - - - Getting License Type %s - - - - - -' %n
                
def GrabLinks():
        for link in BeautifulSoup(browser.page_source).findAll("a"):
                if "agency_id" in link['href']:
                                print link.text
                                url.write(link['href'] + "\n") 
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
                        if len(browser.find_elements_by_link_text("...")) == 1 and i>41:
                                n += 1
                                if n >= 4: # len(licenseTypes)
                                        break
                                else:
                                        GetPage(n)
                                        i = 1
                        elif len(browser.find_elements_by_link_text("...")) == 0:
                                n += 1
                                if n >= 4: # len(licenseTypes)
                                        break
                                else:
                                        GetPage(n)
                                        i = 1
                        elif len(browser.find_elements_by_link_text("..."))==1:
                                browser.find_element_by_link_text("...").click()
                        elif len(browser.find_elements_by_link_text("...")) == 2:
                                browser.find_elements_by_link_text("...")[1].click()
                                
        url.close()

def KSbtp(link):
        print link.replace('\n','')
        try:
                page = s.get("http://licensing.ks.gov/verification/web/" + link.replace('\n',''))
                time.sleep(3)
                soup = BeautifulSoup(re.sub("&amp;", "&", page.content))
                line = []
                line.append("1")
                line.append(soup.find("span", id="_ctl25__ctl1_full_name").text) # entity_name
                line.append(soup.find("span", id="_ctl30__ctl1_addr_city").text) # city
                line.append(soup.find("span", id="_ctl30__ctl1_state").text) # state
                line.append(soup.find("span", id="_ctl30__ctl1_zipcode").text) # zipcode      
                line.append(soup.find("span", id="_ctl35__ctl1_license_no").text) # license_number
                line.append(soup.find("span", id="_ctl35__ctl1_license_type").text) # licensee_type_cd
                line.append(soup.find("span", id="_ctl35__ctl1_status").text) # status
                line.append(soup.find("span", id="_ctl35__ctl1_issue_date").text) # issue_date
                line.append(soup.find("span", id="_ctl35__ctl1_last_ren").text) # renewal_date
                line.append(soup.find("span", id="_ctl35__ctl1_expiry").text) # expiration_date
                line.append(soup.find("span", id="_ctl35__ctl1_obtained_by").text) # obtained_by
                line.append(link.split("=")[-1])
                print line
                f.write("|".join(line) + "\n")
        except:
                if page.status_code != 200:
                        log_list = []
                        log_list.append(url)
                        #subprocess.call(["afplay", pipe])
                        print page.status_code, url
                        log.write("\"" + "\",\"".join(log_list) + "\"\n")
                        pass

def ThreadedScrape():
        links = []
        for line in open("KSbtp_links.csv","r"):
                links.append(line.strip())
        threaded(links, KSbtp, num_threads=3)

def ErrorPass():
        links = []
        for line in open("KSbtp_log.csv","r"):
                links.append(line.strip())
        threaded(links, KSbtp, num_threads=1)
        
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

import json
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re, codecs, time
from thready import threaded
import logging
import subprocess
logging.basicConfig()

log = codecs.open('GApli2_log.csv','w','utf-8')
url = open("GApli_links.csv","w")
f = codecs.open('eng-gen.res-sur_c_GApli_%s_000.txt'%(time.strftime("%Y%m%d")), 'w', 'utf-8')
f.write("company_flag,entity_name,address1,address2,address3,address4,state,zip,profession,license_number,licensee_type_cd,secondary_license,status,first_issue_date,last_renew_date,expiration_date,obatained_by,state_reprosity,url_number".replace(',','|') + "\n")

browser = webdriver.PhantomJS()
s = requests.session()
s.get("http://verify.sos.ga.gov/websites/verification/Search.aspx?facility=Y")
def GetPage(n):
        browser.get("http://verify.sos.ga.gov/websites/verification/Search.aspx?facility=Y")
        time.sleep(3)
        # eng sur: 16, resgen contractor: 42, utility: 49; landscape arch: 23, plumbers: 36
        licenseTypes = [16, 42, 49]
        browser.find_element_by_xpath("//*[@id='t_web_lookup__profession_name']/option[%s]" %(licenseTypes[n])).click()
        time.sleep(3)
        browser.find_element_by_xpath("//*[@id='sch_button']").click()
        print '- - - - - - - Getting License Type %s - - - - - -' %n
        
def NextPage():
        try:
                browser.find_element_by_link_text("%d"%i).click()
        except:
                if len(browser.find_elements_by_link_text("...")) == 1:
                        browser.find_element_by_link_text("...").click()
                elif len(browser.find_elements_by_link_text("...")) == 2:
                        browser.find_elements_by_link_text("...")[1].click()
                

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
                                if n > 2: #len(licenseTypes)
                                        break
                                else:
                                        GetPage(n)
                                        i = 1
                        elif len(browser.find_elements_by_link_text("..."))==1:
                                browser.find_element_by_link_text("...").click()
                        elif len(browser.find_elements_by_link_text("...")) == 2:
                                browser.find_elements_by_link_text("...")[1].click()
                                
        url.close()

def GA_Pli(url):
        try:
                page = s.get("http://verify.sos.ga.gov/websites/verification/" + url)
                time.sleep(3)
                soup = BeautifulSoup(re.sub("&amp;", "&", page.content))
                line = []
                line.append("1")
                line.append(soup.find("span", id="_ctl25__ctl1_full_name").text)
                line.append(soup.find("span", id="_ctl28__ctl1_addr_line_1").text)      
                line.append(soup.find("span", id="_ctl28__ctl1_addr_line_2").text)      
                line.append(soup.find("span", id="_ctl28__ctl1_addr_line_3").text)      
                line.append(soup.find("span", id="_ctl28__ctl1_addr_line_4").text)
                citystatezip = soup.find("span", id="_ctl28__ctl1_addr_line_4").text
                line.append(re.search("[A-Z]{2}",citystatezip).group())
                line.append(re.search("[0-9]{5,}",citystatezip).group())
                line.append(soup.find("span", id="_ctl34__ctl1_profession").text)
                line.append(soup.find("span", id="_ctl34__ctl1_license_no").text)
                line.append(soup.find("span", id="_ctl34__ctl1_license_type").text)
                line.append(soup.find("span", id="_ctl34__ctl1_secondary").text)        
                line.append(soup.find("span", id="_ctl34__ctl1_status").text)
                line.append(soup.find("span", id="_ctl34__ctl1_issue_date").text)
                line.append(soup.find("span", id="_ctl34__ctl1_last_ren").text)
                line.append(soup.find("span", id="_ctl34__ctl1_expiry").text)
                line.append(soup.find("span", id="_ctl34__ctl1_obtained_by").text)
                line.append(soup.find("span", id="_ctl34__ctl1_from_state").text)
                line.append(url.split("=")[-1])
                print line
                #subprocess.call(["say", "I'm taking your fucking data"])
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
        for line in open("GApli_links.csv","r"):
                links.append(line.strip())
        threaded(links, GA_Pli, num_threads=3)

def ErrorPass():
        links = []
        for line in open("GApli2_log.csv","r"):
                links.append(line.strip())
        threaded(links, GA_Pli, num_threads=1)

if __name__ == '__main__':
        n = 0
        GetPage(n)
        ScrapeLinks(n)
        ThreadedScrape()
        ErrorPass()

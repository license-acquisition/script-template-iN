import json
from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import re, codecs, time
from thready import threaded
import logging
import subprocess
from script_template import create_file, logger
logging.basicConfig()

f = create_file('eng-gen.res-sur_c_GApli', 'w', ['6', '12', '0', '1', '2', '3', '36', '44', 'profession', '21', '32', 'secondary_license', '37', '19', '20', '13', 'obatained_by', 'state_reprosity', 'url_number'])
l = logger('eng-gen.res-sur_c_GApli')
g = codecs.open('eng-gen.res-sur_c_GApli', 'w', 'utf-8')
driver = webdriver.PhantomJS()
s = requests.session()
s.get("http://verify.sos.ga.gov/websites/verification/Search.aspx?facility=Y")

def GetPage(n):
        driver.get("http://verify.sos.ga.gov/websites/verification/Search.aspx?facility=Y")
        time.sleep(3)
        # eng sur: 16, resgen contractor: 42, utility: 49; landscape arch: 23, plumbers: 36
        licenseTypes = [16, 42, 49]
        driver.find_element_by_xpath("//*[@id='t_web_lookup__profession_name']/option[%s]" %(licenseTypes[n])).click()
        time.sleep(3)
        driver.find_element_by_xpath("//*[@id='sch_button']").click()
        l.debug('- - - - - - - Getting License Type %s - - - - - -' %n)
        
def NextPage():
        try:
                driver.find_element_by_link_text("%d"%i).click()
        except:
                if len(driver.find_elements_by_link_text("...")) == 1:
                        driver.find_element_by_link_text("...").click()
                elif len(driver.find_elements_by_link_text("...")) == 2:
                        driver.find_elements_by_link_text("...")[1].click()
                

def GrabLinks():
        for link in BeautifulSoup(driver.page_source).findAll("a"):
                if "agency_id" in link['href']:
                                l.info(link.text)
                                g.write(link['href'] + "\n") 
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
                        if len(driver.find_elements_by_link_text("...")) == 1 and i>41:
                                n += 1
                                if n > 2: #len(licenseTypes)
                                        break
                                else:
                                        GetPage(n)
                                        i = 1
                        elif len(driver.find_elements_by_link_text("..."))==1:
                                driver.find_element_by_link_text("...").click()
                        elif len(driver.find_elements_by_link_text("...")) == 2:
                                driver.find_elements_by_link_text("...")[1].click()
        g.close()                        

def GA_Pli(url):
        try:
                page = s.get("http://verify.sos.ga.gov/websites/verification/" + url)
                time.sleep(3)
                soup = BeautifulSoup(re.sub("&amp;", "&", page.content))
                info = []
                info.append("1")
                info.append(soup.find("span", id="_ctl25__ctl1_full_name").text)
                info.append(soup.find("span", id="_ctl28__ctl1_addr_line_1").text)      
                info.append(soup.find("span", id="_ctl28__ctl1_addr_line_2").text)      
                info.append(soup.find("span", id="_ctl28__ctl1_addr_line_3").text)      
                info.append(soup.find("span", id="_ctl28__ctl1_addr_line_4").text)
                citystatezip = soup.find("span", id="_ctl28__ctl1_addr_line_4").text
                info.append(re.search("[A-Z]{2}",citystatezip).group())
                info.append(re.search("[0-9]{5,}",citystatezip).group())
                info.append(soup.find("span", id="_ctl34__ctl1_profession").text)
                info.append(soup.find("span", id="_ctl34__ctl1_license_no").text)
                info.append(soup.find("span", id="_ctl34__ctl1_license_type").text)
                info.append(soup.find("span", id="_ctl34__ctl1_secondary").text)        
                info.append(soup.find("span", id="_ctl34__ctl1_status").text)
                info.append(soup.find("span", id="_ctl34__ctl1_issue_date").text)
                info.append(soup.find("span", id="_ctl34__ctl1_last_ren").text)
                info.append(soup.find("span", id="_ctl34__ctl1_expiry").text)
                info.append(soup.find("span", id="_ctl34__ctl1_obtained_by").text)
                info.append(soup.find("span", id="_ctl34__ctl1_from_state").text)
                info.append(url.split("=")[-1])
                l.info(info)
                #subprocess.call(["say", "I'm taking your fucking data"])
                f.write("|".join(info) + "\n")
        except Exception as e:
                l.error(str(e))


def ThreadedScrape():
        links = []
        for line in open("eng-gen.res_links.csv","r"):
                links.append(line.strip())
        threaded(links, GA_Pli, num_threads=3)

def main():
        n = 0
        GetPage(n)
        ScrapeLinks(n)
        ThreadedScrape()


if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()

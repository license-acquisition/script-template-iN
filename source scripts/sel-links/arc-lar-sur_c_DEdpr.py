#Daryl
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time, re
import codecs
from datetime import date
from glob import glob
from script_template import create_file, logger

f = create_file('arc-lar-sur_c_DEdpr', 'w', ['12', '21', '32', '37', '19', '13', '4', '36', '44', 'country', '102', '6'])
l = logger('arc-lar-sur_c_DEdpr')
driver = webdriver.PhantomJS()

def main():
    page = 1
    count = 1
    link_list = []

    driver.get("https://dpronline.delaware.gov/mylicense%20weblookup/Search.aspx?facility=Y")

    #these are the professions we are interested in
    value = [3,16,17] 
    #the type
    value2 = 38

    for val in value:
        driver.find_elements_by_tag_name("option")[val].click()
        driver.find_elements_by_tag_name("option")[38].click()
        time.sleep(1)
        driver.find_element_by_id("sch_button").click()

        page = 1
        fail = 0 
        while fail == 0:
            try:
                soup = BeautifulSoup(driver.page_source)
                links = soup.findAll("a", href = True)
                for link in links:
                    if "Details" in link['href']:
                        link_list.append(link['href'])

                page += 1
                time.sleep(0.5)

                driver.find_element_by_link_text(str(page)).click()

            except Exception, e:
                l.error(str(e))
                fail += 1
                
        else:
            driver.get("https://dpronline.delaware.gov/mylicense%20weblookup/Search.aspx?facility=Y")
            l.debug('finished getting url from profession' + str(val))


    for x in link_list:

        try:

            url = 'https://dpronline.delaware.gov/mylicense%20weblookup/' + x
            driver.get(url)
            l.info(url)
            info = []
            soup = BeautifulSoup(driver.page_source)
            info.append(soup.findAll("span", {"id" : "_ctl16__ctl1_full_name"})[0].text)
            info.append(soup.findAll("span", {"id" : "_ctl21__ctl1_license_no"})[0].text)
            info.append(soup.findAll("span", {"id" : "_ctl21__ctl1_profession_id"})[0].text)
            info.append(soup.findAll("span", {"id" : "_ctl21__ctl1_sec_lic_status"})[0].text)
            info.append(soup.findAll("span", {"id" : "_ctl21__ctl1_issue_date"})[0].text)
            info.append(soup.findAll("span", {"id" : "_ctl21__ctl1_expiration_date"})[0].text)
            info.append(soup.findAll("span", {"id" : "_ctl26__ctl1_addr_city"})[0].text)
            info.append(soup.findAll("span", {"id" : "_ctl26__ctl1_addr_state"})[0].text)
            info.append(soup.findAll("span", {"id" : "_ctl26__ctl1_addr_zipcode"})[0].text)
            info.append(soup.findAll("span", {"id" : "_ctl26__ctl1_addr_country"})[0].text)
            info.append("license number")
            info.append("1")

            f.write("\"" + "\",\"".join(info) + "\"\n")
            l.info(info)

        except Exception, e:
            l.error(str(e))
            continue

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, codecs
from datetime import date
from script_template import create_file, logger
start = time.time()

# i = 121 end?
f = create_file('asb_c_OHdoh', 'w', [32, 102, 12, 37, 0, 13, 4, 36, 44, 33, 6])
l = logger('OHdoh')
driver  = webdriver.PhantomJS()

def main():
    link_list = []
    i = 7
    page_number = 1
    driver.get('http://publicapps.odh.ohio.gov/Envlicense_Reports/External_License_Search.aspx?Program=Asbestos')
    #driver.find_element_by_id("ctl00_ContentPlaceHolder1_DDLLic_subtype").click()
    #Select(driver.find_element_by_id("ctl00_ContentPlaceHolder1_DDLLic_subtype")).select_by_visible_text("ASBESTOS HAZARD ABATEMENT AIR MONITORING TECHNICIAN")
    #driver.find_element_by_css_selector("option[value=\"6\"]").click()
    driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_DDLLic_subtype"]/option[3]').click()
    time.sleep(5)
    driver.find_element_by_xpath("//*[@id='ContentPlaceHolder1_BtnSubmit']").click()

    """driver.find_element_by_link_text("...").click()

    while page_number <1:
        driver.find_element_by_xpath("(//a[contains(text(),'...')])[2]").click()
        page_number = page_number + 10
        print (page_number)"""
        
    page_number = 1
    #difference should be 11 betweenj the 2 page numbers above
    while page_number < 2460:
        i = 7
        link_list = []
        while i <122:
            try:
                page1 = driver.page_source
                soup = BeautifulSoup(page1)
                links = soup.findAll('td')
                link_list.append(links[i].text)
                i = i + 6
            except:
                i = i+6
        l.info(link_list)


        for link in link_list:
            name = 'NULL'
            lic_type = 'NULL'
            lic_number = 'NULL'
            status = 'NULL'
            address = 'NULL'
            city_state_zip = 'NULL'
            exp = 'NULL'
            phone = 'NULL'
            
            
            try:
                driver.find_element_by_partial_link_text(str(link.strip())).click()
                page = driver.page_source
                soup = BeautifulSoup(page)
                info = []
           #info.append("Licensed Asbestos Contractors")
           #info.append("1")
           #info.append("License Number")
                #info = soup.findAll("td")
                try:
                    lic_type = str(soup.findAll(id="Lbl_License_Desc"))
                    start = lic_type.find('>') + 1
                    end = lic_type[3:].find('<') + 3
                    info.append(lic_type[start:end])
                except:
                    l.error('bad lic_type')
                try:
                    name = str(soup.findAll(id="lbl_Name"))
                    start = name.find('>') + 1
                    end = name[3:].find('<') + 3
                    name = name[start:end]
                    name = re.sub('&amp;','&',name)
                    info.append('license number')
                    info.append(re.sub(',','',name))
                    print (name)         
                except:
                    l.error('bad name')
                try:        
                    lic_number = str(soup.findAll(id="lbl_license_no"))
                    start = lic_number.find('>') + 1
                    end = lic_number[3:].find('<') + 3
                    info.append(lic_number[start:end])        
                except:
                    l.error('bad number')
                try:
                    status = str(soup.findAll(id="lbl_status"))
                    start = status.find('>') + 1
                    end = status[3:].find('<') + 3
                    info.append(status[start:end])
                except:
                    l.error('bad status')
                try:
                    address = str(soup.findAll(id="lbl_Address"))
                    start = address.find('>') + 1
                    end = address[3:].find('<') + 3
                    address = address[start:end]
                    info.append(re.sub(',','',address))
                except:
                    l.error('bad address')
                try:
                    exp = str(soup.findAll(id="lbl_Expire_Date"))
                    start = exp.find('>') + 1
                    end = exp[3:].find('<') + 3
                    info.append(exp[start:end])
                except:
                    l.error('bad exp')
                try:
                    city_state_zip = str(soup.findAll(id="lbl_CityStateZip"))
                    start = city_state_zip.find('>') + 1
                    end = city_state_zip[3:].find('<') + 3
                    citystatezip = city_state_zip[start:end]
                    city = citystatezip.rsplit(",")[0]
                    state = citystatezip.rsplit(",")[1]
                    zipcode = citystatezip.rsplit(" ")[0]
                    info.append(city_state_zip[start:end])
                    info[7] = "\",\"".join(info[7].rsplit(" ", 1))
                    info[7] = "\",\"".join(info[7].rsplit(", ", 1))
                except:
                    l.error('bad city')
                try:
                    phone = str(soup.findAll(id="lbl_Phone"))
                    start = phone.find('>') + 1
                    end = phone[3:].find('<') + 3
                    info.append(phone[start:end])
                except:
                    l.error(':(')
                try:
                    info.append("1")
                    l.info("\"" + "\",\"".join(info) + "\"\n")
                    f.write("\"" + "\",\"".join(info) + "\"\n")    
                except:
                    l.error('could not write name')

                driver.back()
            except:
                l.error('bad link')
        fail = 0
        
        page_number = page_number+1           
        if page_number == 11:
            time.sleep(1)
            driver.find_element_by_partial_link_text("...").click()
            l.info(page_number)
        elif page_number % 10 == 1:    
            driver.find_elements_by_partial_link_text("...")[1].click()                 
            l.info(page_number)       
        else:     
            driver.find_element_by_link_text(str(page_number)).click()
            l.info(page_number)

if __name__ == '__main__':
    try:
        main()
        l.info(str(time.time() - start))
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()

                     

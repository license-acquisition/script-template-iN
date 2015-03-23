from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, codecs
from datetime import date
start = time.time()

link_list = []
i = 7
page_number = 1
# i = 121 end?
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open('asb_c_OHdoh_%s%s%s_000.csv' %(str(year), str(month).zfill(2), str(day).zfill(2)), 'w', 'utf-8')

#f=open('OH Asbestos3.csv','a')
f.write("licensee_type_cd|number_type|entity_name|license_number|status|address1|expiration_date|city|state|zip|phone|company_flag\n")
driver  = webdriver.PhantomJS()
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
    print (link_list)


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
                print ('bad lic_type')
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
                print ('bad name')
            try:        
                lic_number = str(soup.findAll(id="lbl_license_no"))
                start = lic_number.find('>') + 1
                end = lic_number[3:].find('<') + 3
                info.append(lic_number[start:end])
    
            except:
                print ('bad number')
            try:
                status = str(soup.findAll(id="lbl_status"))
                start = status.find('>') + 1
                end = status[3:].find('<') + 3
                info.append(status[start:end])
            except:
                print ('bad status')
            try:
                address = str(soup.findAll(id="lbl_Address"))
                start = address.find('>') + 1
                end = address[3:].find('<') + 3
                address = address[start:end]
                info.append(re.sub(',','',address))
            except:
                print ('bad address')
            try:
                exp = str(soup.findAll(id="lbl_Expire_Date"))
                start = exp.find('>') + 1
                end = exp[3:].find('<') + 3
                info.append(exp[start:end])
            except:
                print ('bad exp')
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
                print ('bad city')
            try:
                phone = str(soup.findAll(id="lbl_Phone"))
                start = phone.find('>') + 1
                end = phone[3:].find('<') + 3
                info.append(phone[start:end])
            except:
                print (':(')
            try:
                info.append("1")
                print("\"" + "\",\"".join(info) + "\"\n")
                f.write("\"" + "\",\"".join(info) + "\"\n")    
            except:
                print ('could not write name')

            driver.back()
        except:
            print ('bad link')
    fail = 0


    page_number = page_number+1

        
    if page_number == 11:
        time.sleep(1)

        driver.find_element_by_partial_link_text("...").click()
        print page_number


    elif page_number % 10 == 1:
  
        driver.find_elements_by_partial_link_text("...")[1].click()
        
       
        print page_number
     
    else:
  
        driver.find_element_by_link_text(str(page_number)).click()
        
        print page_number
 

f.close()

print time.time()-start

                     

#Daryl
#10/15/2014
#chris jimenez 
#re write 2/26/2015

import codecs, time
from selenium import webdriver
from bs4 import BeautifulSoup

f = codecs.open('asb_c_NYdol_%s_000.csv' %time.strftime('%Y%m%d'), 'w', 'utf-8')

f.write("license_number|old license|expiration_date|entity_name|address1|city|state|zip|phone|primary_specialty|company_flag\n")

#Selenium Webdriver
driver = webdriver.Chrome()

#Getting the web page in selenium
driver.get("http://bi.labor.ny.gov/ibmcognos/cgi-bin/cognosisapi.dll?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2fpackage%5b%40name%3d%27WPS%20Reports%27%5d%2freport%5b%40name%3d%27Active%20Asbestos%20Contractors%27%5d&ui.name=Active%20Asbestos%20Contractors&run.outputFormat=&run.prompt=truehttp://bi.labor.ny.gov/ibmcognos/cgi-bin/cognosisapi.dll?b_action=cognosViewer&ui.action=run&ui.object=%2fcontent%2fpackage%5b%40name%3d%27WPS%20Reports%27%5d%2freport%5b%40name%3d%27Active%20Asbestos%20Contractors%27%5d&ui.name=Active%20Asbestos%20Contractors&run.outputFormat=HTML&run.prompt=true&cv.toolbar=false&cv.header=false")

#interacting with elements on the screens
driver.find_elements_by_tag_name("option")[3].click()
driver.find_elements_by_tag_name("button")[0].click()
print "loading page, waiting 25 seconds."
time.sleep(25)

#creating a beautiful soup object.
soup = BeautifulSoup(driver.page_source)
table_items = soup.find_all('span',{'class':'textItem'})
for i in range(0,1000):
    info = []
    license_number          = table_items[17 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    old_license_number      = table_items[18 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    expiration_date         = table_items[19 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    entity_name             = table_items[20 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    address1                = table_items[21 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    city                    = table_items[22 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    state                   = table_items[23 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    zip_code                = table_items[24 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    phone                   = table_items[25 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    abatement               = table_items[27 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    management_planning     = table_items[29 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    monitoring              = table_items[31 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    project_design          = table_items[33 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    inspection              = table_items[35 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    air_monitoring          = table_items[37 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    info.append(license_number)
    info.append(old_license_number)
    info.append(expiration_date)
    info.append(entity_name)
    info.append(address1)
    info.append(city)
    info.append(state)
    info.append(zip_code)
    info.append(phone)
    specialties = ''
    if abatement == 'Yes':
        specialties += 'abatement; '
    if management_planning == 'Yes':
        specialties += 'management planning; '
    if project_design == 'Yes':
        specialties += 'project design'
    if inspection == 'Yes':
        specialties += 'inspection'
    if air_monitoring == 'Yes':
        specialties += 'air monitoring'
    info.append(specialties)
    info.append('1')
    print '|'.join(info)
    f.write('|'.join(info)+'\n')

# Page two
driver.find_element_by_partial_link_text("Page down").click()
print "loading next page, waiting 25 seconds."
time.sleep(25)
soup = BeautifulSoup(driver.page_source)
table_items = soup.find_all('span',{'class':'textItem'})
for i in range(0,549): #change this value once more professionals are added
    info = []
    license_number          = table_items[17 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    old_license_number      = table_items[18 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    expiration_date         = table_items[19 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    entity_name             = table_items[20 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    address1                = table_items[21 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    city                    = table_items[22 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    state                   = table_items[23 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    zip_code                = table_items[24 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    phone                   = table_items[25 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    abatement               = table_items[27 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    management_planning     = table_items[29 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    monitoring              = table_items[31 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    project_design          = table_items[33 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    inspection              = table_items[35 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    air_monitoring          = table_items[37 + i *22].text.replace(u',',' ').replace(u'\xa0',' ')
    info.append(license_number)
    info.append(old_license_number)
    info.append(expiration_date)
    info.append(entity_name)
    info.append(address1)
    info.append(city)
    info.append(state)
    info.append(zip_code)
    info.append(phone)
    specialties = ''
    if abatement == 'Yes':
        specialties += 'abatement; '
    if management_planning == 'Yes':
        specialties += 'management planning; '
    if project_design == 'Yes':
        specialties += 'project design;'
    if inspection == 'Yes':
        specialties += 'inspection;'
    if air_monitoring == 'Yes':
        specialties += 'air monitoring;'
    info.append(specialties)
    print '|'.join(info)
    f.write('|'.join(info)+'\n')

f.close()
driver.close()
driver.quit()



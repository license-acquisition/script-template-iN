from bs4 import BeautifulSoup
import urllib, requests, codecs, re, sys, time
from selenium import webdriver
from glob import glob

#f=open("AL_Scrape6.csv","a")
f = codecs.open('gen_res_c_ALlbg_%s_000.txt' %(time.strftime('%Y%m%d')),'w','utf-8')
headers = ['entity_name', 'license_number', 'address1', 'city', 'state', 'zip', 'phone', 'expiration_date']
f.write('|'.join(headers) + '\n')

url = 'http://genconbd.alabama.gov/DATABASE-SQL/roster.aspx'
short_url = 'http://genconbd.alabama.gov/DATABASE-SQL/'


count = 1
winners = 0
page = 152
# initialize webdriver
driver = webdriver.Chrome()
#driver = webdriver.PhantomJS(glob('C:\\Users\\*\\Downloads\\phantomjs.exe'))
driver.get(url)

# iterate through list
while page < 605:
    print '-'*10
    print page
    print '-'*10
    soup = BeautifulSoup(driver.page_source)
    table = soup.find('table', {'id': 'ctl00_ContentPlaceHolder1_GridView1'})
    links = []
    for link in table.find_all('a'):
        if 'detail' in link['href']:
            detail_url = short_url + link['href']
            stew = BeautifulSoup(requests.get(detail_url).content)
            try:
                info = []
                info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_NameLabel"}).text.strip()) #nameprint soup.find_all("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_NameLabel"}).text.strip()
                info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_LicenseNoLabel"}).text.strip()) #licno
                info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_AddressLabel"}).text.strip()) #address
                info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_CityLabel"}).text.strip()) #city
                info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_StateLabel"}).text.strip()) #state
                info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_ZipLabel"}).text.strip()) #zipcode
                info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_PhonenoLabel"}).text.strip()) #phone
                # info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_FaxLabel"}).text.strip()) #fax
                info.append(stew.find("span", {"id" : "ctl00_ContentPlaceHolder1_FormView1_Expr1Label"}).text.strip()) #expdate
                print info
                f.write('|'.join(info) + '\n')
                winners += 1
            except:
                #print 'Roll Tide bitch'
                print 'fail?z'
                count += 1
                if count%100==0:
                    print 'We\'ve failed quite a bit.'
                    print 'Winners: ' + str(winners)
                    print 'Count: ' + str(count)
    page+=1
    try:                   
        driver.find_element_by_link_text(str(page)).click()
    except:
        if page == 11:
            driver.find_elements_by_link_text('...')[0].click()
        else:
            driver.find_elements_by_link_text('...')[1].click()

f.close()
driver.close()

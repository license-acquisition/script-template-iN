import requests, codecs, time
from bs4 import BeautifulSoup
from selenium import webdriver


f = codecs.open('led.b_c_NCdhs_%s_000.csv' % time.strftime('%Y%m%d'), 'w')
browser = webdriver.PhantomJS()
browser.get('http://www.schs.state.nc.us/lead/accredited.cfm')
headers = ['entitity_name','city','county','state','phone','expiration_date','license_number','company_flag']
f.write("\"" + "\",\"".join(headers) + "\"\n")

browser.find_element_by_name('FSubmit').click()
time.sleep(1)
for i in range(0,2):
    if i == 1:
        browser.find_element_by_xpath('//*[@id="firm_types"]/option[2]').click()
        browser.find_element_by_name('FSubmit').click() 
        time.sleep(1)
    bs = BeautifulSoup(browser.page_source)
    table = bs.find_all('table',{'class','datatableWideLeft'})[1]
    table.find('tr',{'class':'odd'}).extract()
    tds = table.find_all('td')
    for i in range(0,len(tds)/7):
        info = []
        info.append(tds[0 + i * 7].text.strip().replace('\"',''))
        info.append(tds[1 + i * 7].text.strip())
        info.append(tds[2 + i * 7].text.strip())
        info.append(tds[3 + i * 7].text.strip())
        info.append(tds[4 + i * 7].text.strip())
        info.append(tds[5 + i * 7].text.strip())
        info.append(tds[6 + i * 7].text.strip())
        info.append('1')
        f.write("\"" + "\",\"".join(info) + "\"\n")
        print info
    
f.close()
browser.close()
browser.quit()
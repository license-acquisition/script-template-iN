import sys, requests, codecs, time, re, csv, string
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from glob import glob
from string import ascii_letters, digits

date = time.strftime('%Y%m%d')
f = codecs.open('arc_c_ALboa_%s_000.csv' %(date), 'w', 'utf-8')
headers = ["entity_name","address1","city","state","zip","phone","license_number","status","number_type","company_flag","licensee_type_cd","number","qualifying_individual"]
f.write('|'.join(headers) + '\n')
driver = webdriver.PhantomJS()
driver.get("http://www.boa.alabama.gov/COA/COARoster.aspx")

page=1
while True:

    try:
        soup = BeautifulSoup(driver.page_source.replace(u'\xa0',u''))
        table1 = soup.findAll("table", id="ctl00_ContentPlaceHolder1_GridView1")
        i=1
    
        tds = table1[0].find_all('td', {'valign': 'top'})
        for col in table1[0].findAll('td',{"valign":"top", "style":"width: 300px;"}):
            lod = col.text.split('\n')
            info = []
            try:
                info.append(lod[1].replace('\r','').replace(',',' '))    # entity_name
                info.append(lod[2].strip().replace('\r','')) #address1
                city, state = lod[3].split(',')
                info.append(city.strip().replace('\r','')) # city
                info.append(re.search('[A-Z]'*2, state).group()) # state
                info.append(re.search('[0-9]'*5,state).group()) # zip

                info.append(lod[4].strip()) # phone
                qual_ind = lod[5][lod[5].find(re.search('[A-Z][a-z]',lod[5]).group()):]
                number = lod[5][:lod[5].find(re.search('[A-Z][a-z]',lod[5]).group())]
                
                info.append(tds[i].text.replace('\r','').split('\n')[1].strip()) # license_number
                info.append(tds[i].text.replace('\r','').split('\n')[2].strip()) # status
            
                info.append('certification number') # number_type
                info.append('1') # company_flag
                info.append('certificate of authorization') # licensee type code
                info.append(number.replace(u'\xa0',u'')) # number
                info.append(qual_ind.replace(',', ' ').replace(u'\xa0',u' ')) # qualifying individual

                i += 2
                # write it all
                f.write('|'.join(info) + '\n')
                
            except:
                print 'fail'
                pass
            
        page += 1
        if page == 11:
            driver.find_element_by_partial_link_text("...").click()
        elif page % 10 == 1:
            driver.find_elements_by_partial_link_text("...")[1].click()
        else:
            driver.find_element_by_partial_link_text(str(page)).click()
        print page
    except Exception, e:
        print str(e)
        print page
        break
f.close()
driver.close()
driver.quit()
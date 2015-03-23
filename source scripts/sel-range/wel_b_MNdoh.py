from selenium import webdriver
from bs4 import BeautifulSoup
import re
import codecs
from datetime import date
import codecs, time
start = time.time()

browser = webdriver.PhantomJS()

f = codecs.open("wel_b_MNdoh_%s_000.csv" %(time.strftime('%Y%m%d')),"w","utf-8")
headers = ["company_flag","county","entity_name","license_number","licensee_type_cd","address1","city","state","zip","phone","qualifying_individual","qualifying_individual2"]
f.write('|'.join(headers) + '\n')
count = 0

for i in range(2,354):
    try:
        info = []
        browser.get("http://www.health.state.mn.us/divs/eh/wells/lwc/lwcissuenbr.cfm")
        browser.find_element_by_xpath("//*[@id='company_issue_nbr']/option[1]").click()
        numbsearch = browser.find_element_by_xpath("//*[@id='company_issue_nbr']/option[%d]"%i)
        numbsearch.click()
        browser.find_element_by_css_selector("input[type=\"submit\"]").click()
        c = browser.page_source
        soup = BeautifulSoup(c)
        td = soup.findAll("td",{"width":"372"})
        info.append("1")
        info.append(td[0].text.replace(u'\xa0',u''))
        info.append(td[1].text.replace(u'\xa0',u''))
        info.append(td[2].text.strip().replace(u'\xa0',u''))
        info.append(td[3].text.strip().replace(u'\xa0',u''))
        info.append(td[4].text.replace(u'\xa0',u''))
        citystate = td[6].text.replace(u'\xa0',u'').strip()
        city = citystate.split(",")[0]
        statezip = citystate.split(",")[1]
        state = re.search("[A-Z]{2}",citystate).group()
        zipcode = re.search("[0-9]{5}",statezip).group()
        info.append(city.replace(u'\xa0',u''))
        info.append(state.replace(u'\xa0',u''))
        info.append(zipcode.replace(u'\xa0',u''))
        info.append(td[7].text.replace(u'\xa0',u''))
        for names in soup.findAll("table",{"width":"100%", "cellpadding":"5","class":"table_background_shade"}):
            indname = names.findAll("td")
            for ok in indname:
                info.append(ok.text.replace("&nbsp;",""))
        print info
        f.write("|".join(info) + "\n")
    except:
        print browser.current_url
        count = count + 1
        print count

f.write(time.time()-start)
f.close()
browser.quit()

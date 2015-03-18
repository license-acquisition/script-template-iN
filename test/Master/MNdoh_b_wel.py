from selenium import webdriver
from bs4 import BeautifulSoup
import re
import codecs
from datetime import date
import codecs, time
from script_template import create_file, logger

start = time.time()
browser = webdriver.PhantomJS()

f = create_file('wel_b_MNdoh', 'w', [6, 8, 12, 21, 32, 1, 4, 36, 44, 33, 35, 'qualifying_individual2'])
l = logger('MNdoh')

count = 0
def main():
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
            l.info(info)
            f.write("|".join(info) + "\n")
        except Exception as e:
            l.info(browser.current_url)
            count = count + 1
            l.error(str(e))
        finally:
            f.close()
            browser.quit()
    l.info('COMPLETE')
    l.info(str(time.time() - start))

if __name__ == '__main__':
        main()

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import codecs
from datetime import date
import codecs, time
from script_template import create_file, logger

f = create_file('wel_b_MNdoh', 'w', [6, 8, 12, 21, 32, 1, 4, 36, 44, 33, 35, 'qualifying_individual2'])
l = logger('wel_b_MNdoh')
driver = webdriver.PhantomJS()

count = 0
def main():
    for i in range(2,354):
        try:
            info = []
            driver.get("http://www.health.state.mn.us/divs/eh/wells/lwc/lwcissuenbr.cfm")
            driver.find_element_by_xpath("//*[@id='company_issue_nbr']/option[1]").click()
            numbsearch = driver.find_element_by_xpath("//*[@id='company_issue_nbr']/option[%d]"%i)
            numbsearch.click()
            driver.find_element_by_css_selector("input[type=\"submit\"]").click()
            soup = BeautifulSoup(driver.page_source)
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
            l.info(driver.current_url)
            l.error(str(e))
    

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()

import requests, codecs, time, logging
from string import ascii_lowercase
from bs4 import BeautifulSoup
from selenium import webdriver
from itertools import product
from script_template import create_file, logger

f = create_file('gen.res_c_MDllr', 'w', ['7', '0', '4', '36', '44', '13', '32', '21'])
l = logger('gen.res_c_MDllr')
driver = webdriver.PhantomJS()

# Requires 3 letters for inclusive search, hit most common and de-dupe until consistent final #
def main():
        keywords = [''.join(i) for i in product(ascii_lowercase, repeat =3)]

        for lictype in ['AR', 'LA', 'LS']: # original ['AR', 'LA','LS']
                for term in keywords:
                        l.debug(' - - - - Searching %s: %s - - - - - ' %(lictype, term))
                        driver.get('https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=%s::%s_business_name' %(lictype, lictype))
                        driver.find_element_by_css_selector("input[name=businessname]").send_keys("%s" %term)
                        driver.find_element_by_css_selector("input[name=Submit]").click()
                        while True:
                                try:
                                        for tr in BeautifulSoup(driver.page_source).find("table",{"border":"4"}).findAll("tr")[1:]:
                                                info = []
                                                for td in tr.findAll("td"):
                                                        info.append(td.text.strip())
                                                l.info(info)
                                                f.write("|".join(info).replace("&amp;", "&") + "\n")
                                                del(info)
                                        driver.find_element_by_css_selector("input[value=' Next 50 ']").click()
                                except:
                                        break

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
###################################
# Output: led_c_KSdoh
# Method: selenium, single-page
###################################

from script_template import create_file, logger
from bs4 import BeautifulSoup
from selenium import webdriver

f = create_file('led_c_KSdoh', 'w', [6, 36, 8, 4, 12, 0, 33, 21, 32, 32, 'name'])
l = logger('KSdoh')

driver = webdriver.PhantomJS

def main():
    l.info('starting scrape...')
    driver.get('http://kensas.kdhe.state.ks.us/leadRegistry/getActiveLeadRegistryFirms.kdhe')
    driver.find_elements_by_tag_name("input")[1].click()
    driver.find_elements_by_tag_name("input")[-1].click()
    
    soup = BeautifulSoup(driver.page_source.replace("<br />", "_%_").replace("</b>","").replace("<br>","_%_"))
    info = []
    try:
        for tr in soup.find("table", {"border":"2"}).findAll("tr")[1:]:
                info.append("1")	
                for td in tr.findAll("td"):
                        info.append(td.text.replace("\"", "").replace("_%_", "\",\"").replace("&amp;", "&").replace("\n", "").strip())
                l.info(info)
                # mp
                f.write('|'.join(info) + '\n')
                info = []
    except Exception as e:
        l.critical(str(info[4]))
        l.critical(str(e))

if __name__ == '__main__':
    try:
        main()
        l.info('COMPLETE')
    except Exception as e:
        l.critical(str(e))
    finally:
        driver.quit()
        f.close()

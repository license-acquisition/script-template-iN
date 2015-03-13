###################################
# Output: led_c_KSdoh
# Method: selenium, single-page
###################################

from script_template import create_file
from bs4 import BeautifulSoup
from selenium import webdriver
from script_template import logger

def main():
    f = create_file('led_c_KSdoh', 'w', [6, 36, 8, 4, 12, 0, 33, 21, 32, 32, 'name'])
    logger(f.name, 'START')
    driver = webdriver.PhantomJS()
    try:
        driver.get("http://kensas.kdhe.state.ks.us/leadRegistry/getActiveLeadRegistryFirmSearchForm.kdhe")
        driver.find_elements_by_tag_name("input")[1].click()
        driver.find_elements_by_tag_name("input")[-1].click()

        info = []
        for tr in BeautifulSoup(driver.page_source.replace("<br />", "_%_").replace("</b>","").replace("<br>","_%_")).find("table", {"border":"2"}).findAll("tr")[1:]:
                info.append("1")	
                for td in tr.findAll("td"):
                        info.append(td.text.replace("\"", "").replace("_%_", "\",\"").replace("&amp;", "&").replace("\n", "").strip())
                print info
                f.write('|'.join(info) + '\n')
                info = []
        logger(f.name, 'COMPLETE')
    except:
        logger(f.name, 'ERROR', str(info[0]))
        pass
    finally:
        f.close()
        driver.quit()



if __name__ == '__main__':
    main()

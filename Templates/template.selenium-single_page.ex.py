###################################
# Output: led_c_KSdoh
# Method: selenium, single-page
###################################

from script_template import create_file
from bs4 import BeautifulSoup
from selenium import webdriver
from script_template.feed_log import logger

#headers = ['company_flag', 'state', 'county', 'city', 'entity_name', 'address1', 'phone', 'license_number', 'licensee_type_cd', 'licensee_type_cd', 'name']

def main():
    logger(f.name, 'START')
    f = create_file('led_c_KSdoh', 'w', [1,2,3,4,5,6,7,8,9,10])
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

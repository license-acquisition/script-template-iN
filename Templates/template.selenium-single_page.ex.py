###################################
# Output: led_c_KSdoh
# Method: selenium, single-page
###################################

from script_template import create_file
from bs4 import BeautifulSoup
from selenium import webdriver

f = create_file('led_c_KSdoh', 'w', [6, 36, 8, 4, 12, 0, 33, 21, 32, 32, 'name'])
driver = webdriver.PhantomJS()

def main():

    driver.get("http://kensas.kdhe.state.ks.us/leadRegistry/getActiveLeadRegistryFirmSearchForm.kdhe")
    driver.find_elements_by_tag_name("input")[1].click()
    driver.find_elements_by_tag_name("input")[-1].click()

    info = []
    for tr in BeautifulSoup(driver.page_source.replace("<br />", "_%_").replace("</b>","").replace("<br>","_%_")).find("table", {"border":"2"}).findAll("tr")[1:]:
            info.append("1")	
            for td in tr.findAll("td"):
                    info.append(td.text.replace("\"", "").replace("_%_", "\",\"").replace("&amp;", "&").replace("\n", "").strip())
            h.info(info)
            f.write('|'.join(info) + '\n')
            info = []

if __name__ == '__main__':
    try:
        main()
    except Exception, e:
        print str(e)
    finally:
        f.close()
        driver.quit()

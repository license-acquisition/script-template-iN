#only works with IE driver or Firefox driver (downgraded version: 28.0)
from bs4 import BeautifulSoup
from selenium import webdriver
import string
from datetime import date
import re, time
import codecs
from script_template import create_file, logger

f = create_file('ele_c_RIdlt', 'w', ['32', '63', '12', '0', '4', '36', '44', '33', '21', 'description', '19', '13', '6'])
l = logger('ele_c_RIdlt')
driver = webdriver.Firefox()

def main():
        driver.get("http://www.dlt.ri.gov/profregsonline/PROLentree1.aspx")
        driver.find_elements_by_tag_name("input")[14].click()
        time.sleep(3)
        for i in string.ascii_lowercase:
                driver.find_element_by_id("txtCorpName").send_keys("%s"%i)
                driver.find_element_by_id("btnName").click()
                try:
                        k = 1
                        while k < 10:
                                for j in range(0,9):
                                        try:
                                                driver.find_element_by_id("DGcorp").find_elements_by_tag_name("input")[j].click()
                                                info = []
                                                info.append("Electrical Corporation")
                                                try:
                                                        alert = driver.switch_to_alert()
                                                        print alert.text
                                                        info.append(alert.text)
                                                        alert.dismiss()
                                                except:
                                                        info.append("")
                                                soup = BeautifulSoup(driver.page_source)
                                                info.append(soup.findAll("span",{"id":"lblCorp"})[0].text.strip())
                                                info.append(soup.findAll("span",{"id":"lblStreet"})[0].text.strip())
                                                info.append(soup.findAll("span",{"id":"lblCityData"})[0].text.strip())
                                                info.append(soup.findAll("span",{"id":"lblStateData"})[0].text.strip())
                                                info.append(soup.findAll("span",{"id":"lblZip"})[0].text.strip())
                                                info.append(soup.findAll("span",{"id":"lblAreaCodeData"})[0].text.strip())
                                                info.append(soup.findAll("span",{"id":"lblLicenseNumber"})[0].text.strip())
                                                info.append(soup.findAll("span",{"id":"lblDescription"})[0].text.strip())
                                                info.append(soup.findAll("span",{"id":"lblIssueDate"})[0].text.strip())
                                                info.append(soup.findAll("span",{"id":"lblExpDate"})[0].text.strip())
                                                info.append("1")
                                                info.append(soup.findAll("span",{"id":"lblTelephone"})[0].text.strip())
                                                info[7] = info[7] + info[13]
                                                info[13] = ''
                                                f.write("\"" + "\",\"".join(info) + "\"\n")
                                                l.info(info)
                                                driver.find_element_by_id("btnPrev").click()
                                                #driver.back()
                                        except Exception, e:
                                                l.error('Level 1: ' + str(e))
                                k = k + 1
                                try:
                                        driver.find_element_by_link_text("%s"%k).click()
                                except:
                                        driver.find_element_by_xpath("//*[@id='btnNewSearch']").click()
                except Exception, e:
                        l.error('Level 2: '+str(e))



if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()

#only works with IE driver or Firefox driver (downgraded version: 28.0)
from bs4 import BeautifulSoup
from selenium import webdriver
import string
from datetime import date
import re, time
import codecs
year = date.today().year
month = date.today().month
day = date.today().day
f = codecs.open("ele_c_RIdlt_%s%s%s_000.csv" %(str(year), str(month).zfill(2), str(day).zfill(2)),"w","utf-8")
f.write("license_type_cd,disciplinary_string,entity_name,address1,city,state,zip,phone,license_number,description,first_issue_date,expiration_date,company_flag\n")
#f = open("RIalarm.csv", "w")
#DGalarmco$ctl10$ctl00
browser = webdriver.Firefox()
browser.get("http://www.dlt.ri.gov/profregsonline/PROLentree1.aspx")
browser.find_elements_by_tag_name("input")[14].click()
time.sleep(3)
for i in string.ascii_lowercase:
        browser.find_element_by_id("txtCorpName").send_keys("%s"%i)
        browser.find_element_by_id("btnName").click()
        try:
                k = 1
                while k < 10:
                        for j in range(0,9):
                                try:
                                        browser.find_element_by_id("DGcorp").find_elements_by_tag_name("input")[j].click()
                                        info = []
                                        info.append("Electrical Corporation")
                                        try:
                                                alert = browser.switch_to_alert()
                                                print alert.text
                                                info.append(alert.text)
                                                alert.dismiss()
                                        except:
                                                info.append("")
                                        soup = BeautifulSoup(browser.page_source)
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
                                        print "\"" + "\",\"".join(info) + "\"\n"
                                        browser.find_element_by_id("btnPrev").click()
                                        #browser.back()
                                except Exception, e:
                                        print str(e)
                        k = k + 1
                        try:
                                browser.find_element_by_link_text("%s"%k).click()
                        except:
                                browser.find_element_by_xpath("//*[@id='btnNewSearch']").click()
        except Exception, e:
                print str(e)



f.close()
browser.close()
browser.quit()

# only works with ie driver or firefox driver
from bs4 import BeautifulSoup
from selenium import webdriver
import string
from datetime import date
import re, time
import codecs
from script_template import create_file, logger

f = create_file('sec_c_RIdlt', 'w', ['32', '63', '21', '13', '20', '12', '0', '4', '36', '44', '33', '10', '35', 'Middle', 'Last', '37', '6'])
l = logger('sec_c_RIdlt')
driver = webdriver.Firefox()

def main():
	driver.get("http://www.dlt.ri.gov/profregsonline/PROLentree1.aspx")
	driver.find_elements_by_tag_name("input")[7].click()
	time.sleep(3)
	for i in string.ascii_lowercase:
		driver.find_element_by_id("txtLastName").send_keys("%s"%i)
		driver.find_element_by_id("btnName").click()
		try:
			k = 1
			while k < 10:
				for j in range(0,9):
					try:			
						driver.find_element_by_id("DGalarmco").find_elements_by_tag_name("input")[j].click()
						info = []
						info.append("Licensed Alarm Company")
						try:
							alert = driver.switch_to_alert()
							l.debug(alert.text)
							info.append(alert.text)
							alert.dismiss()
						except:
							info.append("")
						soup = BeautifulSoup(driver.page_source)
						info.append(soup.findAll("span",{"id":"lblLicNumber"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"lblLicExpData"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"lblRenewalDate"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"LblAgency"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"LblAgncyStreet"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"LblAgncyCity"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"LblAgncyState"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"LblAgncyZip"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"LblAgncyTelephone"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"LblDBAdata"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"lblFirst"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"lblMiddle"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"lblLast"})[0].text.strip())
						info.append(soup.findAll("span",{"id":"LblStatusData"})[0].text.strip())
						info[12] = (info[12] + " " + info[13] + " " + info[14])
						info.append("1")
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
			l.error('Level 2: ' + str(e))



if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
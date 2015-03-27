# Kyle
# Uses URLs pulled by grabbing them
import time, re, requests, codecs
from glob import glob
from selenium import webdriver
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('pes_c_ALdai', 'w', ['35', '7', '8', '0', '4', '36', '44', '21', '13', '22', '32', '6'])
l = logger('pes_c_ALdai')
g = codecs.open('pes_c_ALdai_links.csv', 'w', 'utf-8')
driver = webdriver.PhantomJS()

# Private or Commercial
driver.get("http://agi-app.alabama.gov/Commercial.aspx")
driver.find_element_by_id("ctl00_ContentPlaceHolder2_btnSearch").click()
i = 2
while i < 531:
	for link in BeautifulSoup(driver.page_source).findAll("a"):
		try:
			if "Details" in link['href']:
				g.write(link['href'] + "\n")
		except:
			pass
	if i == 11:
		driver.find_element_by_link_text("...").click()
	elif i % 10 == 1:
		driver.find_elements_by_link_text("...")[1].click()
	else:
		driver.find_element_by_link_text("%s"%i).click()
	i += 1
	
l.info('finished grabbing links')

tally = 0
for line in open("pes_c_ALdai_links.csv", "r"):
	info = []
	for td in BeautifulSoup(requests.get("http://agi-app.alabama.gov/%s"%line).content.replace("<br>", "\",\"")).findAll("td", {"style":"font-size: x-small;"})[1::2]:
		info.append(td.text)
	info[3] = re.sub("(?<!\"),", "", "\",\"".join(info[3].rsplit(" ", 2)))
	info.append('1')
	f.write("|".join(info) + "\n")
        tally+=1

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
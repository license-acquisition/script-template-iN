import sys, re, requests, codecs, csv
from bs4 import BeautifulSoup
from glob import glob
from selenium import webdriver
from datetime import date
from script_template import create_file, logger

f = create_file('sur_c_FLdcs', 'w', ['10', '7', '91', '33', '32', '21', '19', '13', '37', '22', '27', 'issue_date2', '14', '38', '23', '28', 'issue_date3', '15', '39', '24', '29', 'issue_date4', '16', '40', '25', '30', 'issue_date5', '17', '41', '6', '102'])
l = logger('sur_c_FLdcs')
driver = webdriver.PhantomJS()

def main():
	driver.get("https://csapp.800helpfla.com/cspublicapp/businesssearch/businesssearch.aspx")
	driver.find_element_by_css_selector("option[value=LB]").click()
	driver.find_element_by_css_selector("input[value='Search']").click()
	driver.find_element_by_css_selector("option[value=ALL]").click()
	soup = BeautifulSoup(driver.page_source)

	i = 0
	while i < 1408:
		
		table1 = soup.find("table", id="cpMainContent_MasterGv_main_%d"%i)
		tablei = table1.find_all("table")[0]
		tableii = table1.find_all("table")[2]

		data = []
		tr = table1.find_all("td")[-1].text
		if "DBA/Other Names" in tr:
			tr = tr.replace ("DBA/Other Names", "")
			data.append(tr.strip())
		else:
			data.append(" ")
		for td in tablei.find_all("td"):
			data.append(td.text.strip())
		for bold in tableii.find_all("strong"):
			bold.decompose()
		for td in tableii.find_all("td"):
			data.append(td.text)

		data = "\",\"".join(data).replace("Phone", "\",\"")
		data = data.split("\",\"")

		try:
			del(data[4])
			del(data[4])
			del(data[4])
			del(data[4])
			del(data[4])		
		except:
			pass
		line =  '\"' + '\",\"'.join(data) + "\"\n"
		line = re.sub("\s\s*", " ", line)
		
		l.info(line + "\n")
		f.write(line + "\n")
		i += 1

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
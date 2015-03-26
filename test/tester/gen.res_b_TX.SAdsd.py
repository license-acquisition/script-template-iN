import codecs, re, csv, time, requests
from bs4 import BeautifulSoup
from selenium import webdriver
from script_template import create_file, logger

f = create_file('gen.res_b_TX.SAdsd', 'w', ['no headers'])
l = logger('TX.SAdsd')
s = requests.session()
driver = webdriver.PhantomJS()

def main():
        i=1
        while i < 39: 	
                driver.get("https://webapps1.sanantonio.gov/bils/index.aspx")
                soup = BeautifulSoup(driver.page_source)
                #for option, a in enumerate(soup.find_all("option")):
                #	print a.text
                #	print option
                option = driver.find_elements_by_tag_name("option")[i]
                name = option.text
                option.click()
                driver.find_element_by_css_selector("input[value='Find Record']").click()
                soup = BeautifulSoup(driver.page_source)
                i+=1
                j=2
                while True:
                        for tr in soup.find("table", id="DataGrid1").find_all("tr")[1:-1]:
                                payload = []
                                for td in tr.find_all("td"):
                                        payload.append(td.text.strip())
                                f.write('\"' + "\",\"".join(payload) + "\"\n")
                                l.info('\"' + "\",\"".join(payload) + "\"\n")
                        try:
                                if j == 11:
                                        driver.find_elements_by_partial_link_text("...")[0].click()
                                elif j % 10 == 1:
                                        driver.find_elements_by_partial_link_text("...")[1].click()
                                else:	
                                        driver.find_element_by_partial_link_text(str(j)).click()
                                time.sleep(3)
                                j+=1
                                soup = BeautifulSoup(driver.page_source)
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
	


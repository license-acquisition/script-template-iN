from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from script_template import create_file, logger

f = create_file('led_c_RIdoh','w',[])
l = logger('RIdoh')
browser = webdriver.PhantomJS()


def main():
	browser.get("http://209.222.157.144/RIDOH_Verification/Search.aspx?facility=Y&SubmitComplaint=Y")
	browser.find_elements_by_css_selector("option")[35].click()
	browser.find_element_by_css_selector("input[value='Search']").click()
	j=2
	while j < 52:
		try:
			for i in range(3, 43):
				print i
				fail = 0
				while fail == 0:
					try:	
						browser.find_element_by_css_selector('a[id=datagrid_results__ctl%d_hl]'%i).click()
						#time.sleep(.5)
						browser.switch_to_window(browser.window_handles[-1])
						
						data = []
						try:
							try:
								element = WebDriverWait(browser, 10).until(
								    EC.presence_of_element_located((By.ID, "full_name"))
								)
							finally:
								pass
							soup = BeautifulSoup(browser.page_source)
							data.append(soup.find("span", {"id" : "full_name"}).text)
							try:
								data.append(soup.find("span", {"id" : "_ctl19__ctl1_addr_line_1"}).text)
								data.append(soup.find("span", {"id" : "_ctl19__ctl1_line_4"}).text)
							except:
								data.append(" ")
								data.append(" ")
							data.append(soup.find("span", {"id" : "_ctl25__ctl1_license_no"}).text)
							data.append(soup.find("span", {"id" : "_ctl25__ctl1_profession_id"}).text)
							data.append(soup.find("span", {"id" : "_ctl25__ctl1_license_type"}).text)
							data.append(soup.find("span", {"id" : "_ctl25__ctl1_sec_lic_status"}).text)
							data.append(soup.find("span", {"id" : "_ctl25__ctl1_issue_date"}).text)
							data.append(soup.find("span", {"id" : "_ctl25__ctl1_expiration_date"}).text)
							data.append(soup.find("span", {"id" : "_ctl25__ctl1_sec_license_type"}).text)
							f.write("|".join(data) + "\n")
							print ('\"' + '\"\n\"'.join(data))	
						except Exception as e:
							print data			    
							print str(e)
						browser.close()
						browser.switch_to_window(browser.window_handles[0])
						fail = 1
						
					except Exception as e:
				    
						print str(e)
			if j == 41:
				browser.find_elements_by_partial_link_text("...")[0].click()
			elif j % 40 == 1:
				browser.find_elements_by_partial_link_text("...")[1].click()
			else:	
				browser.find_element_by_partial_link_text(str(j)).click()
			j = j + 1
		except Exception, e:
			print str(e)


if __name__ == '__main__':
	try:
		main()
	except Exception, e:
		l.critical(str(e))
	finally:
		f.close()

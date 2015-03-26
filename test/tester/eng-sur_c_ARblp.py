#----------------------
# Don Lawson
# 6/24/2014
# AR Engineers and Surveyors
#--------------
# RANGE:
# - Search Results (ALL Firms)
# METHODS:
# - Selenium-->PhantomJS
#-----------------------

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from sys import stdout
from glob import glob
import re, time
from script_template import create_file, logger

#takes a float value of progress (current over total) and
#outputs a progress bar with running percentage on a single line
def update_progress(progress):
        barLength = 50
        if isinstance(progress, int):
                progress = float(progress)
        if not isinstance(progress,float):
                progress = 0
        block = int (round(barLength*progress))
        text = "[{0}] {1}%".format("="*block + "-"*(barLength-block),progress*100)
        stdout.write('\r%s' %text)
        stdout.flush()

f = create_file('eng-sur_c_ARblb', 'w', [7, 0, 4, 36, 44, 21, 13])
driver = webdriver.PhantomJS()

def main():
        driver.get('http://www.arkansas.gov/pels/search/search.php')
        driver.find_element_by_css_selector("input[type='radio'][value='firms']").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        i = 0

        l.debug("\nMagic is happening...\n")
        try:
                while driver.find_element_by_xpath('//*[@id="app_form"]/table/tbody/tr[1]/td[3]/a'): # Next 20 >>
                        sauce = BeautifulSoup(driver.page_source)
                        table = sauce.find("table",{'class':'renewal_results'})
                        #print table
                        info = []
                
                        for tr in table.find_all('tr')[2:-3]:
                                tds = tr.find_all('td')
                                info.append(tds[0].text.strip()) # company_name
                                addr = str(tds[1]).split('<br>')
                                if 'CANADA' in addr[2]: # filter for Canadian addresses
                                        info.append(addr[0][addr[0].find('>')+1:]) # address1
                                        info.append(addr[1].split(',')[0].split(' ')[0]) # city
                                        info.append(addr[1].split(',')[0].split(' ')[1]) # state
                                        info.append(addr[1].split(',')[1].strip()) # zip
                                else:
                                        info.append(addr[0][addr[0].find('>')+1:]) # address1
                                        info.append(addr[1].split(',')[0]) # city
                                        info.append(re.search(r'[A-Za-z]'*2, addr[1].split(',')[1]).group()) # state
                                        info.append(re.search(r'[0-9]'*5, addr[1].split(',')[1]).group()) # zip
                                info.append(tds[2].text.strip()) # license_number
                                info.append(tds[3].text.strip()) # expiration_date

                                # write to file and empty info list
                                f.write('|'.join(info) +'\n')
                                
                                info = []
                        # go to next page
                        driver.find_element_by_xpath('//*[@id="app_form"]/table/tbody/tr[1]/td[3]/a').click()
                        i+=1
                        print i
                        # progress bar
                        soup = BeautifulSoup(driver.page_source)
                        info_text = soup.find('table',{'class':'renewal_results'}).findAll('tr')[0].findAll('td')[1].text
                        pages = [int(s) for s in info_text.split() if s.isdigit()]
                        current = pages[1]
                        total = pages[2]
                        page_progress = float(current)/float(total)
                        update_progress(page_progress)
                        

        except Exception as e:
                l.error('whoops')
                l.error(i)
                l.error(str(e))

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()

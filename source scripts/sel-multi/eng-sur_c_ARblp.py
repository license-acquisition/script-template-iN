#----------------------
# Don Lawson
# 6/24/2014
# AR Engineers and Surveyors
#--------------
# RANGE:
# - Search Results (ALL Firms)
# METHODS:
# - Selenium-->PhantomJS
# CSV FILE NAME:
# - eng-sur_c_ARblb-20140624_000.csv
#-----------------------
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from sys import stdout
from glob import glob
import re, time
from script_template import create_file, logger

f = create_file('eng-sur_c_ARblp', 'w', ['7', '0', '4', '36', '44', '21', '13'])
l = logger('eng-sur_c_ARblp')
driver = webdriver.PhantomJS()

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


def main():
        driver.get('http://www.arkansas.gov/pels/search/search.php')
        driver.find_element_by_css_selector("input[type='radio'][value='firms']").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        i = 0

        try:
                while driver.find_element_by_xpath('//*[@id="app_form"]/table/tbody/tr[1]/td[3]/a'): # Next 20 >>
                        soup = BeautifulSoup(driver.page_source.replace('<br>', '|').replace('</br>','|'))
                        table = soup.find("table",{'class':'renewal_results'})
                        l.debug(len(table.find_all('tr')[2:-3]))
                        info = []
                
                        for tr in table.find_all('tr')[2:-3]:
                                tds = tr.find_all('td')
                                l.debug(len(tds))
                                info.append(tds[0].text.strip()) # company_name
                                addr = tds[1].text.split('|')
                                l.debug(addr)
                                if 'CANADA' in addr[2]: # filter for Canadian addresses
                                        pass
                                else:
                                        info.append(addr[0].strip()) # address1
                                        info.append(addr[1].rsplit(' ', 2)[-1])
                                        info.append(addr[1].rsplit(' ', 2)[-2])
                                        info.append(addr[1].rsplit(' ', 2)[0].replace(',', '').strip())
                                info.append(tds[2].text.strip()) # license_number
                                info.append(tds[3].text.strip()) # expiration_date

                                # write to file and empty info list
                                f.write('|'.join(info) +'\n')
                                l.info(info)
                                info = []
                        # go to next page
                        driver.find_element_by_xpath('//*[@id="app_form"]/table/tbody/tr[1]/td[3]/a').click()
                        i+=1
                        l.debug(i)
                        '''
                        # progress bar
                        soup = BeautifulSoup(driver.page_source)
                        info_text = soup.find('table',{'class':'renewal_results'}).findAll('tr')[0].findAll('td')[1].text
                        pages = [int(s) for s in info_text.split() if s.isdigit()]
                        current = pages[1]
                        total = pages[2]
                        page_progress = float(current)/float(total)
                        update_progress(page_progress)
                        '''

        except Exception as e:
                l.error(str(e))
                l.error(i)

        
if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception, e:
                l.critical(str(e))
        finally:
                f.close()
                driver.quit()
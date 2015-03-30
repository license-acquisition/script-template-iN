import requests, codecs, time
from bs4 import BeautifulSoup
from selenium import webdriver
from script_template import create_file, logger

f = create_file('led.b_c_NCdhs', 'w', ['12', '4', '8', '36', '33', '13', '21', '6'])
l = logger('led.b_c_NCdhs')
driver = webdriver.PhantomJS()

def main():
    driver.get('http://www.schs.state.nc.us/lead/accredited.cfm')
    driver.find_element_by_name('FSubmit').click()
    time.sleep(1)
    for i in range(0,2):
        if i == 1:
            driver.find_element_by_xpath('//*[@id="firm_types"]/option[2]').click()
            driver.find_element_by_name('FSubmit').click() 
            time.sleep(1)
        bs = BeautifulSoup(driver.page_source)
        table = bs.find_all('table',{'class','datatableWideLeft'})[1]
        table.find('tr',{'class':'odd'}).extract()
        tds = table.find_all('td')
        for i in range(0,len(tds)/7):
            info = []
            info.append(tds[0 + i * 7].text.strip().replace('\"',''))
            info.append(tds[1 + i * 7].text.strip())
            info.append(tds[2 + i * 7].text.strip())
            info.append(tds[3 + i * 7].text.strip())
            info.append(tds[4 + i * 7].text.strip())
            info.append(tds[5 + i * 7].text.strip())
            info.append(tds[6 + i * 7].text.strip())
            info.append('1')
            f.write("\"" + "\",\"".join(info) + "\"\n")
            l.info(info)
    

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()
        driver.quit()
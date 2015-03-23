import requests, codecs, time, logging
from string import ascii_lowercase
from bs4 import BeautifulSoup
from selenium import webdriver
from thready import threaded
logging.basicConfig()

start = time.time()
f = codecs.open("gen.res_c_MDllr_%s_000.txt"%(time.strftime('%Y%m%d')), 'w', 'utf-8')
f.write("name,trade_name,address,city,state,zip,expiration_date,category,license_number,suffix".replace(",","|") + "\n")

# Requires 3 letters for inclusive search, hit most common and de-dupe until consistent final #

browser = webdriver.PhantomJS()

#def MDllr(url):
for lictype in ['LA', 'LS']: # original ['AR', 'LA','LS']
        for i in ascii_lowercase:
                for j in ascii_lowercase:
                        for k in ascii_lowercase:
                                print ' - - - - Searching %s: %s%s%s - - - - - ' %(lictype, i,j,k)
                                browser.get('https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=%s::%s_business_name' %(lictype, lictype))
                                browser.find_element_by_css_selector("input[name=businessname]").send_keys("%s%s%s"%(i,j,k))
                                browser.find_element_by_css_selector("input[name=Submit]").click()
                                while True:
                                        try:
                                                for tr in BeautifulSoup(browser.page_source).find("table",{"border":"4"}).findAll("tr")[1:]:
                                                        info = []
                                                        for td in tr.findAll("td"):
                                                                info.append(td.text.strip())
                                                        print info
                                                        f.write("|".join(info).replace("&amp;", "&") + "\n")
                                                        del(info)
                                                browser.find_element_by_css_selector("input[value=' Next 50 ']").click()
                                        except:
                                                break
'''
def threaded_scrape():
        links = []
        for lictype in ['AR', 'LA', 'LS']:
                links.append('https://www.dllr.state.md.us/cgi-bin/ElectronicLicensing/OP_Search/OP_search.cgi?calling_app=%s::%s_business_name' %(lictype, lictype))
        threaded(links, MDllr, num_threads=3)
'''
#threaded_scrape()
f.write('It actually finished. \n')
f.write('Minutes elapsed: %s' %((time.time() - start)/60))
f.close()

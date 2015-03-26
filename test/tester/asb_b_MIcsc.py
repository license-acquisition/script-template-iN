#******************* METHOD 1: Using Beautiful Soup and Requests ******************

import csv, re, requests, time, string, codecs # for CSV files, Regex, getting URLs, time data, string has useful features like the alphabet, codecs.open can "Open an encoded file using the given mode and return a wrapped version providing transparent encoding/decoding."
from bs4 import BeautifulSoup # for parsing HTML
from script_template import create_file, logger

#--------------------- Name the File You Want to Put Your Data Into ---------------

f = create_file('asb_b_MIcsc', 'w', [12, 36, 44, 33, 32, 21, 37,"", 13])
l = logger('MIcsc')

#------------------------------- Get URL to Scrape --------------------------------

def main():
        largeGap = 1000
        gap = 0
        i = 0
        while True:
                try:
                        i += 1
                        gap +=1
                        if gap > largeGap * 2 or i > 10000:
                                break

                        url = 'http://www.dleg.state.mi.us/asbestos_program/dt_contractor.asp?id=%d' % i
                        soup = BeautifulSoup(requests.get(url).content)

                        # Parse
                        tables = soup.find('div', align = 'center').find_all('table')

                        info = []
                        for tr in tables[0].find_all('tr')[1:]:
                                info.append(tr.find_all('td')[2].text.replace(u'\xa0',u''))

                        for td in tables[1].find_all('tr')[2].find_all('td'):
                                info.append(td.text.strip().replace(u'\xa0',u''))

                        f.write("\"" + "\",\"".join(info) + "\"\n")
                        l.info("\"" + "\",\"".join(info) + "\"\n")
                        l.info('-' * 50)
                        info = []

                        if gap > largeGap:
                                largeGap = gap
                                
                        gap = 0


                except Exception as e:
                        l.error(str(e))
                        l.error("KHAN!!!!!!!!!!!!!!!!!")
                        l.error('-' * 25)

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()

import requests, re, codecs, time
from bs4 import BeautifulSoup as soupify
from selenium import webdriver
from script_template import create_file, logger

# create file
f = create_file('fur_b_c_CAear', 'w', ['12', '32', '21', 'Registry', '37', '0', '4', '44', '8', '12', '32', '21', 'Registry', '13', '19', '4', '36', '44', '8', 'Action'])
l = logger('fur_b_c_CAear')

def main():
  # set up some stuffz
  check = True
  start = 1
  tally, count = 0, 0
  short_url = 'http://www2.dca.ca.gov/pls/wllpub/'
  url = 'http://www2.dca.ca.gov/pls/wllpub/WLLQRYNA$LCEV2.QueryList'
  payload = {'P_QTE_CODE': 'LIC',
         'P_QTE_PGM_CODE': '5710',
         'P_NAME': '',
         'P_CITY': '',
         'P_COUNTY': '',
         'P_RECORD_SET_SIZE': '500',
         'Z_START': '1',
         'Z_ACTION': 'Find'}
  s = requests.Session()
  s.get('http://www2.dca.ca.gov/pls/wllpub/wllqryna$lcev2.startup?p_qte_code=LIC&p_qte_pgm_code=5710') # initialize session
  # loop through 500s until dead
  fails = 0
  while check:
      payload['Z_START'] = str(start)
      try:
          # get soup
          l.debug('Sending request...')
          soup = soupify(requests.get(url, params=payload).content)
          # scrape all the info from data table
          for tr in soup.find_all('table')[0].find_all('tr')[1:]:
              l.debug(' - - - - - %s of %s - - - - -' %(count, tally))
              info1 = []
              for td in tr.find_all('td'):
                  info1.append(td.text.strip())
                  # find href and get all data from that specific company
                  try:
                      if td.find('a')['href'] != '#':
                          soup = soupify(requests.get(short_url + td.find('a')['href']).content)
                          info2 = []
                          for tr in soup.find_all('tr', {'valign': 'TOP'}):
                              info2.append(tr.find_all('td')[1].text.strip())
                  except Exception as e:
                      l.error(str(e))
              # write to file
              f.write('|'.join(info1) + '|' + '|'.join(info2) + '\n')
              l.info(info1 + info2)
              count += 1
              tally += 1
      except Exception as e:
          l.error(str(e))
          tally += 1
          fails += 1
      start += 500
      if fails > 10:
          check = False

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e: l.critical(str(e))
    finally: f.close()

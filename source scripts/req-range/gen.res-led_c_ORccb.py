import sys, requests, codecs, time, re, csv, string
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('gen.res_c_ORccb', 'w', ['21', '37', '19', '12', '6', '0', '4', '44', '33', '32', '78', '80'])
l = logger('gen.res_c_ORccb')

def main():
    s = requests.session()
    s.get("http://search.ccb.state.or.us/search/")

    for i in range (1,250000):
        url = "http://www.ccb.state.or.us/search/search_results.asp?regno=%6d" %i
        page = s.get(url)
        soup = BeautifulSoup(page.content)
        url2 = "http://www.ccb.state.or.us/search/business_detail.asp?license_number=%6d" %i
        try:
            info2 = []
            info = []

            data = soup.findAll('tr',{"class":"bodyText"})
            for tex in data:
                for texto in tex.findAll('td'):
                    info2.append((texto.text).strip())
                    
            info.append(info2[2])
            info.append(info2[5])
            info.append(info2[7])
            info.append(info2[9])
            info.append("1")
            
            if len(info)>2:
                page2 = s.get(url2)
                soup = BeautifulSoup(page2.content)

                data2 = soup.findAll('td',{"colspan":"3"})

                info.append((data2[2].text).strip())
                info.append((data2[3].text).strip())
                info.append((data2[4].text).strip())

                info[5] = "|".join(info[5].rsplit(" ",1))
                info[5] = "|".join(info[5].rsplit(" ",1))
                info[7] = (re.sub('\r\n','',info[7]))
                try: 
                    info[7] = "|".join(info[7].split(":",1))
                    info[7] = "|".join(info[7].rsplit("Commercial:",1))
                except:
                    continue

                info[7] = info[7].strip()

                l.info(info)
                f.write ("|".join(info) + "\n")

            else:
                continue

        except Exception, e:
            l.error(str(e))
         
                
if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
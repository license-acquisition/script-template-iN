import sys, requests, codecs, re, csv, time
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('gen.res_b_WVdlc', 'w', ['21', '6', '10', '0', '4', '36', '44', '8', '33', '32', '13', '102'])
l = logger('gen.res_b_WVdlc')

def main():
    for i in range(1,744):
        try:
            url = "http://www.wvlabor.com/newwebsite/Pages/contractor_RESULTS.cfm?PageNum_WVNUMBER=%d&wvnumber=&contractor_name=&dba=&city_name=&County=&Submit3=Search+Contractors" %i
            soup = BeautifulSoup(requests.get(url).content)
            trs = soup.find_all("tr")
            del(trs[0])
            del(trs[len(trs) - 1])
            for tr in trs:
                tds = tr.find_all("td")
                try: 
                    info = []
                    info.append(str(tds[0].text)) #WVNumber
                    info.append(str(tds[1].text)) #Company
                    info.append(str(tds[2].text)) #Dba
                    info.append(str(tds[3].text)) #address
                    info.append(str(tds[4].text)) #city
                    info.append(tds[5].text) #state
                    info.append(tds[6].text) #zip
                    info.append(tds[7].text) #county
                    info.append(tds[8].text) #phone
                    info.append(tds[9].text) #licensee_type_cd
                    info.append(tds[10].text) #expires
                    info.append("License Number") #number_type
                    f.write("|".join(info) + "\n")
                    l.info(info)
                               
                except Exception as e: 
                    l.error(str(e))   
                    continue
        except Exception as e:
            l.error(str(e))
            continue

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()

    
    

import sys, requests, codecs, re, csv, time
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger
start=time.time()

f = create_file('gen.res_b_WVdlc', 'w', [21, 6, 10, 0, 4, 36, 44, 8, 33, 32, 13, 102])

def main():
    for i in range(1,743):
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
                        WVNumber = str(tds[0].get_text())
                        info.append(WVNumber)

                        Company = str(tds[1].get_text())
                        info.append(Company)

                        DBA = str(tds[2].get_text())
                        info.append(DBA)

                        Address = str(tds[3].get_text())
                        info.append(Address)

                        City = str(tds[4].get_text())
                        info.append(City)

                        State = tds[5].get_text()
                        info.append(State)

                        Zip = tds[6].get_text()
                        info.append(Zip)

                        County = tds[7].get_text()
                        info.append(County)

                        Phone = tds[8].get_text()
                        info.append(Phone)

                        licensee_type_cd = tds[9].get_text()
                        info.append(licensee_type_cd)

                        Expires = tds[10].get_text()
                        info.append(Expires)
                        
                        numbertype = "License Number"   
                        info.append(numbertype)

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
        l.info(str(time.time() - start))
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
    
    

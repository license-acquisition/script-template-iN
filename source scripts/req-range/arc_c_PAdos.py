import sys, requests, codecs, time, re, csv, string
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits
from script_template import create_file, logger

f = create_file('arc_c_PA', 'w', ['12', '4', '36', '44', '32', '21', '', 'professions', '37', '19', '13', '20', '6'])
l = logger('arc_c_PA')

s = requests.session()
s.get("http://www.licensepa.state.pa.us/Search.aspx?facility=Y")


def main():
    for i in range (30000,35000):
        url = "http://www.licensepa.state.pa.us/Details.aspx?agency_id=1&license_id=%d&"%i
        page=s.get(url)
        time.sleep(1)
        soup = BeautifulSoup(page.content)
        
        try:
            info = []
            info.append((soup.find("span", id="_ctl17__ctl1_full_name")).text)
            info.append((soup.find("span", id="_ctl22__ctl1_addr_line_4")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_license_type")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_license_no")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_sec_license_type")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_profession_id")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_sec_lic_status")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_Issue_Date")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_Expiration_Date")).text)
            info.append((soup.find("span", id="_ctl27__ctl1_date_last_renewal")).text)
            info.append("1")

            info[1] = "|".join(info[1].rsplit(" ", 1))
            info[1] = "|".join(info[1].rsplit(" ", 1))
            

        except Exception, e:
            l.error(str(e))
            l.debug(str(i))
            continue  
        l.info(info)
        f.write("|".join(info) + "\n")

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
#download
#
#http://www.wvpebd.org/Portals/WVPEBD/docs/ACTIVE_COAs_Roster.pdf
#rename Active_coas_roster.pdf to well.pdf
#have fun

import requests, re, time
from subprocess import call
from bs4 import BeautifulSoup
#g = open("well.pdf", "w")
#g.write(requests.get("http://www.wvpebd.org/Portals/WVPEBD/docs/ACTIVE_COAs_Roster.pdf").content)
#g.close()
call(["pdftotext", "-layout", "well.pdf"],shell=True)

f = open("eng_c_WVrpe_%s_000.csv"%time.strftime("%Y%m%d"), "w")
headers = ['WV COA#','entity_name','address','city','state','zip','engineer-in-charge','wv pe#','coa expiration date']
f.write("\"" + "\"|\"".join(headers) + "\"\n")
for line in open("well.txt", "r"):
        if "Address" not in line:
                nline = re.sub("   *", "_%_", line)
                nline = re.sub("\n", "", nline)
                nline = nline.split("_%_")
                
                if len(nline) == 10:
                        nline[2] = nline[2] + " " + nline[3]
                        del(nline[3])
                if len(nline) >= 6:
                        f.write("\"" + "\"|\"".join(nline) + "\"\n")

f.close()

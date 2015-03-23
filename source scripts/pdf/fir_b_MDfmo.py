#**************************
# Scrape of MD Fire Spinkler Contractor PDF
# Download PDF from: https://www.mdsp.org/Organization/StateFireMarshal/CodeEnforcementLicensingRegulation/SprinklerContractors.aspx

# Anthony Nault
# 08/21/2014
#**************************

# NOTE: pdftotext is not working on my Mac... But this code seems to work fine on other systems like Linux. The problem when I try to run it is that the text conversion does not preserve alignement in the data :( -Anthony

import requests, re, sys, time, codecs
from subprocess import call
from bs4 import BeautifulSoup
'''
# Find link to download PDF
url = 'https://www.mdsp.org/Organization/StateFireMarshal/CodeEnforcementLicensingRegulation/SprinklerContractors.aspx'
page = requests.get(url)
soup = BeautifulSoup(page.content)
links = soup.find_all('a')
contractor_link = ""
for link in links:
        if link.text == "Sprinkler Contractor Approved Listing":
                contractor_link = link['href']
if contractor_link == "":
        sys.exit("FATAL ERROR! PDF not found. Check source link for changes.")
url = 'https://www.mdsp.org' + contractor_link

# Download PDF
url = 'https://www.mdsp.org/LinkClick.aspx?fileticket=QG1QDiUyq00%3d&tabid=614'
open('fir_b_MDfmo.pdf', 'w').write(requests.get(url).content)

# Convert PDF to text
call(["pdftotext", "-layout", "-table", "fir_b_MDfmo.pdf"])
'''
f = codecs.open("fir_b_MDfmo_%s_000.txt" %(time.strftime('%Y%m%d')), "w", 'utf-8')

headers = ["license_number", "expiration_date", "entity_name", "address1", "city", "state", "zip", "phone", "licensee_type_cd", "qualifying_individual", "company_flag"]
f.write("|".join(headers) + "\n")

info = []
for line in codecs.open("fir_b_MDfmo.txt", "r").readlines():
        if 'Maryland State Fire' not in line and 'Licensed Sprinkler' not in line and 'License  #' not in line and 'of 5' not in line:
                if len(line) != 0:
                        data = line.replace('\n','').split('  ')
                        for d in data:
                                info.append(d.strip())
                        info = [x for x in info if len(x) != 0]
                        if len(info) > 1:
                                info.append('1')
                                f.write('|'.join(info) + '\n')
                                print info
                                info = []
                        
f.close()







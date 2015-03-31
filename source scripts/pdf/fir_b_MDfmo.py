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
from script_template import create_file, logger

f = create_file('fir_b_MDfmo', 'w', ['21', '13', '12', '0', '4', '36', '44', '33', '32', '35', '6'])
l = logger('fir_b_MDfmo')

def main():
        #open('fir_b_MDfmo.pdf', 'wb').write(requests.get('https://www.mdsp.org/LinkClick.aspx?fileticket=QG1QDiUyq00%3d&tabid=614').content)
        call(["pdftotext", "-layout", "-table", "fir_b_MDfmo.pdf"])

        info = []
        for line in open('fir_b_MDfmo.txt', 'r'):
                if 'Maryland State Fire' not in line and 'Licensed Sprinkler' not in line and 'License  #' not in line and 'of 5' not in line:
                        if len(line) != 0:
                                data = line.replace('\n','').split('  ')
                                for d in data:
                                        info.append(d.strip())
                                info = [x for x in info if len(x) != 0]
                                if len(info) > 1:
                                        info.append('1')
                                        f.write('|'.join(info) + '\n')
                                        l.info(info)
                                        info = []
                        

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
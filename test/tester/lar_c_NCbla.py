#####################
# North Carolina Lanscape Architects
# Business Name, Address, State, Zip , Phone, Fax, Email, License #, First Date, Thru Date
# From: http://www.ncbola.org/architect_directory.lasso?p=%x&-session=LASession:PeLUdqrXPI5kTja0YRmsjwLI4yzO7135864E21
#####################

import requests, time
import re
from bs4 import BeautifulSoup
import codecs
from script_template import create_file, logger

f = create_file('lar_c_NCbla', 'w', [12, 0, 33, 66, 43, 21, 19, 13,])
l = logger('NCbla')

def main():
        formline = ["", "", "", "", "", "", "", ""]

        for x in range(1,10):
                url = "http://www.ncbola.org/firm_directory.lasso?p=%s-session=LASession:iN6yt9vSnd9LYORCHj1Vau6sgOxU3114A71423" %x
                soup = BeautifulSoup(requests.get(url).content.replace('<br>', '|').replace('\n',''))
                divs = soup.find_all('div', {'class': 'directoryitem'})
                for div in divs:
                        info = div.text.split('|')
                        for i in range(len(info)):
                                try:
                                        if 'ebsite' not in info[i]:
                                                info[i] = info[i].split(':')[1].strip()
                                        else:
                                                info[i] = info[i].split('ebsite:')[1].strip()
                                except:
                                        pass
                        l.info(info)
                        f.write('|'.join(info) + '\n')
                        
if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()

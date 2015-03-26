import sys, requests, codecs, time, re, csv, string
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits
from script_template import create_file, logger

f = create_file('arc_b_ORbae', 'w', ['12', '21', '37', '62', '0', '4', '36', '44', '19', '13', 'HSW', '6', '32'])
l = logger('arc_b_ORbae')

def main():
    url='http://orbae.com/database/search_architects.php?status=Active&fname=&mi=&lname=&firm=&license=&city=&state=&option=com_content&task=view&id=20&Itemid=1'
    soup=BeautifulSoup(requests.get(url).content.replace("<br>"," "))

    #grab the html for the page
    info=[]
    td=soup.findAll('td')
    i=0
    try:
        for one in td[1::6]:
            info.append(one.text)
            
            two=td[2+(6*i)].text
            info.append(two)
            
            three=td[3+(6*i)].text.replace(",","")
            three="|".join(three.rsplit(" ", 3))
            info.append(three)
            
            four=td[4+(6*i)].text
            d=four[0:10]
            e=four[10:]
            info.append(d)
            info.append(e)
            
            five=td[5+(6*i)].text
            info.append(five)

            part1 = "|".join(info[0].rsplit(" ",1))
            info[1] = "|".join(info[1].rsplit(" ",1))

            determineCom = info[0].rsplit("(",1)
            if "AF" in determineCom[1]:
                info.append("1")
                info.append("Architecture Firm")
            
            l.info(info)
            f.write("|".join(info) + "\n")
            info=[]
            i += 1
    except Exception as e:
        l.error(str(e))
    
if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()

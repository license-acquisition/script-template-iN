import sys, requests, codecs, time, re, csv, string
from bs4 import BeautifulSoup
from datetime import date
from string import ascii_letters, digits
from script_template import create_file, logger

f = create_file('arc_b_ORbae', 'w', [12, 21, 37, 'disciplinary_status', 0, 36, 44, 19, 13, 'HSW', 6, 32])
l = logger('ORbae')

def main():
    #grab the html for the page
    url='http://orbae.com/database/search_architects.php?status=Active&fname=&mi=&lname=&firm=&license=&city=&state=&option=com_content&task=view&id=20&Itemid=1'
    soup=BeautifulSoup(requests.get(url).content.replace("<br>"," "))

    list1=[]
    td=soup.findAll('td')
    i=0
    for one in td[1::6]:
        list1.append(one.text)
        
        two=td[2+(6*i)].text
        list1.append(two)
        
        three=td[3+(6*i)].text.replace(",","")
        three="\",\"".join(three.rsplit(" ", 3))
        list1.append(three)
        
        four=td[4+(6*i)].text
        d=four[0:10]
        e=four[10:]
        list1.append(d)
        list1.append(e)
        
        five=td[5+(6*i)].text
        list1.append(five)

        part1 = "|".join(list1[0].rsplit(" ",1))
        list1[1] = "|".join(list1[1].rsplit(" ",1))

        determineCom = list1[0].rsplit("(",1)
        if "AF" in determineCom[1]:
            list1.append("1")
            list1.append("Architecture Firm")
        
        l.info("\"" + "\",\"".join(list1) + "\"\n")
        f.write("|".join(list1) + "\n")
        list1=[]
        i=i+1
    
f.close()
if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close

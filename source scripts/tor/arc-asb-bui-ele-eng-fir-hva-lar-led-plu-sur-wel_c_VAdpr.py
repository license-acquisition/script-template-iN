#contractors 27010, 27051,
#pip install PySocks
#Download latest Tor Browser
#add the following code to the torrc file located in Browser/TorBrowser/Data/Tor/torrc:
#MaxCircuitDirtiness NUM.   (set num to number of seconds between each enforced IP change.)
#(this cycle proxies faster/renews identity) Default is 10 mins.So reduce it.
#Connect/Open to Tor Browser
#Run the script.
import requests
from bs4 import BeautifulSoup
import codecs
import time
import socks
import socket
# This makes sure that all connections from within this script use the local SOCKS proxy
#(which is initiated by Tor and runs on port 9150)
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
import urllib2
stamp = time.strftime("%Y%m%d")
f=codecs.open("gen.res.a_c_VA_%s_000.csv"%(stamp),"a","utf-8")
f.write("company_flag,entity_name,dba,license_number,licensee_type_cd,firm_type,rank,address1,city,state,zip,specialties,first_issue_date,expiration_date\n")

#set range 
for i in range(1,40101):
    try:
        info = []
        url = "http://dporweb.dpor.virginia.gov/LicenseLookup/LicenseDetail?l=27010%05d"%i
        source = requests.get(url)
        print url
        #perform a simple connection test
        print(urllib2.urlopen('http://icanhazip.com').read())
        soup = BeautifulSoup(source.content)
        info = []
        variety = soup.findAll("strong")
        iWant = variety[2].text
        if len(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})) == 9:
            print "hello"
            info.append("1")
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[0].text.replace("\r\n\t","").replace("\r\n",""))
            if variety[2].text != "DBA Name":
                info.append("") #name
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[1].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[2].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[3].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[4].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[5].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[6].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[7].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[8].text.replace("\r\n\t","").replace("\r\n",""))
            info[7] = "\",\"".join(info[7].rsplit(" ", 1))
            info[7] = "\",\"".join(info[7].rsplit(", ", 2))
            print("\"" + "\",\"".join(info) + "\"\n")
            f.write("\"" + "\",\"".join(info) + "\"\n")
        elif len(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})) == 8:
            print "hello"
            info.append("1")
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[0].text.replace("\r\n\t","").replace("\r\n",""))
            info.append("") #name
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[1].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[2].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[3].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[4].text.replace("\r\n\t","").replace("\r\n",""))    
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[5].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[6].text.replace("\r\n\t","").replace("\r\n",""))
            info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[7].text.replace("\r\n\t","").replace("\r\n",""))
            
            info[7] = "\",\"".join(info[7].rsplit(" ", 1))
            info[7] = "\",\"".join(info[7].rsplit(", ", 2))
            print("\"" + "\",\"".join(info) + "\"\n")
            f.write("\"" + "\",\"".join(info) + "\"\n")
        elif len(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})) == 10:
            if iWant=="DBA Name":
                
                info.append("1")
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[0].text.replace("\r\n\t","").replace("\r\n","")) #name
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[1].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[2].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[3].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[4].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[5].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[6].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[7].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[8].text.replace("\r\n\t","").replace("\r\n",""))
                info[7] = "\",\"".join(info[7].rsplit(" ", 1))
                info[7] = "\",\"".join(info[7].rsplit(", ", 2))
                print("\"" + "\",\"".join(info) + "\"\n")
                f.write("\"" + "\",\"".join(info) + "\"\n")
            elif iWant=="License Number":             
                print "hello 3"
                info.append("1")
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[0].text.replace("\r\n\t","").replace("\r\n","")) #name
                info.append("")
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[1].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[2].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[3].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[4].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[5].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[6].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[7].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[8].text.replace("\r\n\t","").replace("\r\n",""))
                info[7] = "\",\"".join(info[7].rsplit(" ", 1))
                info[7] = "\",\"".join(info[7].rsplit(", ", 2))
                print("\"" + "\",\"".join(info) + "\"\n")
                f.write("\"" + "\",\"".join(info) + "\"\n") 
        elif len(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})) == 11:
            if iWant=="DBA Name":
                
                info.append("1")
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[0].text.replace("\r\n\t","").replace("\r\n","")) #name
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[1].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[2].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[3].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[4].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[5].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[6].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[7].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[8].text.replace("\r\n\t","").replace("\r\n",""))
                info[7] = "\",\"".join(info[7].rsplit(" ", 1))
                info[7] = "\",\"".join(info[7].rsplit(", ", 2))
                print("\"" + "\",\"".join(info) + "\"\n")
                f.write("\"" + "\",\"".join(info) + "\"\n")
            elif iWant=="License Number":             
                print "hello 3"
                info.append("1")
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[0].text.replace("\r\n\t","").replace("\r\n","")) #name
                info.append("")
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[1].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[2].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[3].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[4].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[5].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[6].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[7].text.replace("\r\n\t","").replace("\r\n",""))
                info.append(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})[8].text.replace("\r\n\t","").replace("\r\n",""))
                info[7] = "\",\"".join(info[7].rsplit(" ", 1))
                info[7] = "\",\"".join(info[7].rsplit(", ", 2))
                print("\"" + "\",\"".join(info) + "\"\n")
                f.write("\"" + "\",\"".join(info) + "\"\n") 
        else:
                pass


        def update_progress(progress):
            barLength = 50
            if isinstance(progress, int):
                progress = float(progress)
            if not isinstance(progress,float):
                progress = 0
        block = int (round(barLength*progress))
        text = "[{0}] {1}%".format("="*block + "-"*(barLength-block),progress*100)
        stdout.write('\r%s' %text)
        stdout.flush()
    except Exception, e:
        print "%d"%i
f.close()

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
from script_template import create_file, logger
# This makes sure that all connections from within this script use the local SOCKS proxy
#(which is initiated by Tor and runs on port 9150)
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9150)
socket.socket = socks.socksocket
import urllib2

f = create_file('gen.res.a_c_VA', 'w', ['6', '12', '10', '21', '32', 'firm_type', 'rank', '0', '4', '36', '44', '78', '19', '13']
l = logger('gen.res.a_c_VA')

def main():
    #set range 
    for i in range(1,40101):
        try:
            info = []
            url = "http://dporweb.dpor.virginia.gov/LicenseLookup/LicenseDetail?l=27010%05d"%i
            source = requests.get(url)
            l.debug(url)
            #perform a simple connection test
            l.debug(urllib2.urlopen('http://icanhazip.com').read())
            soup = BeautifulSoup(source.content)
            info = []
            variety = soup.findAll("strong")
            iWant = variety[2].text
            if len(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})) == 9:
                l.debug("hello")
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
                l.info(info)
                f.write("\"" + "\",\"".join(info) + "\"\n")
            elif len(soup.findAll("div",{"class":"col-sm-6 col-xs-11"})) == 8:
                l.debug("hello")
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
                l.info(info)
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
                    l.info(info)
                    f.write("\"" + "\",\"".join(info) + "\"\n")
                elif iWant=="License Number":             
                    l.debug("hello 3")
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
                    l.info(info)
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
                    l.info(info)
                    f.write("\"" + "\",\"".join(info) + "\"\n")
                elif iWant=="License Number":             
                    l.debug("hello 3")
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
                    l.info(info)
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
            l.error(i)
            l.error(str(e))


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()

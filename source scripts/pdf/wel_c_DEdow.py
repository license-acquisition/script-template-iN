import requests, re, time, codecs
from subprocess import call
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('wel_c_DEdow', 'w', ['21', '12', '33', '0', '4', '36', '44'])
l = logger('wel_c_DEdow')

def main():
        open("wel_c_DEdow.pdf", "wb").write(requests.get("http://www.dnrec.delaware.gov/wr/Information/WaterSupplyInfo/Documents/2013%20Licensed%20Water%20Well%20Contractors.pdf").content)
        call(["pdftotext", "-layout", "-table", "wel_c_DEdow.pdf"])

        lines = codecs.open('wel_c_DEdow.txt', 'r').readlines()
        infoLine = []
        for i in range(len(lines)):
                if len(lines[i]) > 1 and not any(s in lines[i] for s in ['State','Commercially','(Excludes','Please Note','Updated']):
                        infoLine.append(lines[i])

        for line in infoLine:
                data = re.split(r'\s{2,}', line)
                print data
                f.write('|'.join(data))
 


if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                print str(e)
                l.critical(str(e))
        finally:
                f.close()


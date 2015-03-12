############################
# Output: wel_c_DEdow
# Method: PDF
############################

import codecs, requests, re, time
from subprocess import call
from script_template import create_file

f = create_file('wel_c_DEdow', 'w', [1,2,3,4,5,6,7,8,9,10])

def log(status):
    feed = 'wel_c_DEdow_%s_000.txt' %(time.strftime('%Y%m%d'))
    l = codecs.open('log.csv', 'a')
    l.write(','.join([feed, str(time.strftime('%Y/%m/%d')), str(time.time()), status]) + '\n')

open("wel_c_DEdow.pdf", "w").write(requests.get("http://www.dnrec.delaware.gov/wr/Information/WaterSupplyInfo/Documents/2013%20Licensed%20Water%20Well%20Contractors.pdf").content)
call(["pdftotext", "-layout", "-table", "wel_c_DEdow.pdf"]) # for windows, pdf2text.py

def main():
    for line in open("wel_c_DEdow.txt", "r"):
            nline = re.sub("   *", "_%_", line)
            nline = re.sub("\n", "", nline)
            nline = nline.split("_%_")
            if len(nline) > 4:
                    f.write('|'.join(nline)+'\n')

# Main Logic # # # # # # # # # # #
if __name__ == '__main__':
    log('START')
    try:        
        main()
        log('COMPLETE')
    except: log('ERROR')
    finally: f.close()

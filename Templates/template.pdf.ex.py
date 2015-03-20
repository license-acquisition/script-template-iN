import requests, re
from subprocess import call
from script_template import create_file, logger

f = create_file('wel_c_DEdow', 'w', [1,2,3,4,5,6,7,8,9,10])
l = logger('DEdow')

def main():
    open("wel_c_DEdow.pdf", "w").write(requests.get("http://www.dnrec.delaware.gov/wr/Information/WaterSupplyInfo/Documents/2013%20Licensed%20Water%20Well%20Contractors.pdf").content)
    call(["pdftotext", "-layout", "-table", "wel_c_DEdow.pdf"])
    for line in open("wel_c_DEdow.txt", "r"):
            nline = re.sub("   *", "_%_", line)
            nline = re.sub("\n", "", nline)
            nline = nline.split("_%_")
            if len(nline) > 4:
                    f.write('|'.join(nline)+'\n')

# Main Logic # # # # # # # # # # #
if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception, e:
        l.critical(str(e))
    finally:
        f.close()

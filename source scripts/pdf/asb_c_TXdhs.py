#download AsbestosConsultantAgencies.pdf at:
# http://www.dshs.state.tx.us/WorkArea/linkit.aspx?LinkIdentifier=id&ItemID=54848
import requests, re, codecs, time
from subprocess import call
from script_template import create_file, logger

f = create_file('asb_c_TXdhs', 'w', ['file_number', '21', '12', '0', '4', '36', '44', '8', '33', '13', '37', '19', 'rank_date'])
l = logger('asb_c_TXdhs')

def main():
    call(["pdftotext","-layout", "-table","asb_c_TXdhs.pdf"])

    for line in open("asb_c_TXdhs.txt", "r"):
    	if "Phone" not in line:
    		nline = re.sub("   *","_%_", line)
    		nline = re.sub("\n", "", nline)
    		nline = nline.split("_%_")
    		if len(nline) > 10:
    			f.write("|".join(nline) + "\n")
    			l.info(nline)

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
        call(['rm', 'asb_c_TXdhs.pdf'])
        call(['rm', 'asb_c_TXdhs.txt'])
    except Exception as e:
        l.critical(str(e))
    finally: 
        f.close()
	
#download LeadFirm.pdf at:
# http://www.dshs.state.tx.us/WorkArea/linkit.aspx?LinkIdentifier=id&ItemID=8589968560
import requests, re, codecs, time
from bs4 import BeautifulSoup
from subprocess import call
from script_template import create_file, logger

f = create_file('led_c_TXdhs', 'w', ['file_number', '21', '12', '0', '4', '36', '44', '8', '33', '13', '37', '19', 'rank_date'])
l = logger('led_c_TXdhs')

def main():
	call(["pdftotext","-layout","led_c_TXdhs.pdf"], shell=True)

	for line in open("led_c_TXdhs.txt","r"):
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
	except Exception as e:
		l.critical(str(e))
	finally:
		f.close()
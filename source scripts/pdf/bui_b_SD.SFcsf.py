from subprocess import call
import re
import requests
from bs4 import BeautifulSoup
import codecs
from datetime import date
import codecs, time
from script_template import create_file, logger

f = create_file('bui_b_SD.SFcsf', 'w', ['32', '21', '12', '0', '4', '36', '44', '33', '33', '35', '102', '6'])
l = logger('bui_b_SD.SFcsf')

#http://www.siouxfalls.org/planning-building/building/electrical.aspx
#http://www.siouxfalls.org/planning-building/building/building.aspx
#http://www.siouxfalls.org/planning-building/building/mechanical.aspx

def main():
	pdfs = ['bui_b_SD.SFcsf.pdf', 'ele_b_SD.SFcsf.pdf', 'plu_b_SD.SFcsf.pdf']
	texts = ['bui_b_SD.SFcsf.txt', 'ele_b_SD.SFcsf.txt', 'plu_b_SD.SFcsf.txt']
	for i in range(3):
		call(["pdftotext", "-layout", "-table", pdfs[i]])

		for line in open(texts[i], "r"):
			nline = re.sub("   *", "_%_", line)
			nline = re.sub("\n", "", nline)
			nline = nline.split("_%_")
			nline.append("License")
			nline.append("1")
			if len(nline) == 11:
				nline[6] = (nline[6] + nline[7])
				state = nline[4].split(",")[1]
				nline[4] = nline[4].split(",")[0]
				nline.insert(5,state)
				l.info(nline)
				f.write("|".join(nline) + "\n")

if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception as e:
		l.critical(str(e))
	finally:
		f.close()
import requests, re, time
from subprocess import call
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('eng_c_WVrpe', 'w', ['WV COA#', '12', '0', '4', '36', '44', 'engineer-in-charge', 'wv pe#', 'coa expiration date'])
l = logger('eng_c_WVrpe')

def main():
        open('eng_c_WVrpe.pdf', 'wb').write(requests.get("http://www.wvpebd.org/Portals/WVPEBD/docs/ACTIVE_COAs_Roster.pdf").content)
        call(["pdftotext", "-layout", "-table", "eng_c_WVrpe.pdf"])

        for line in open("eng_c_WVrpe.txt", "r"):
                if "Address" not in line:
                        nline = re.sub("   *", "_%_", line)
                        nline = re.sub("\n", "", nline)
                        nline = nline.split("_%_")
                        
                        if len(nline) == 10:
                                nline[2] = nline[2] + " " + nline[3]
                                del(nline[3])
                        if len(nline) >= 6:
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

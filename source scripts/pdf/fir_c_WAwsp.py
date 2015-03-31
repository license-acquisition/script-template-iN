import requests, re
from subprocess import call
import requests
import time
from script_template import create_file, logger

f = create_file('fir_c_WAwsp', 'w', ['7', 'address1/city', 'Contact', '13', 'Level', '21', 'state/zip', '33'])
l = logger('fir_c_WAwsp')

def main():
	open("fir_c_WAwsp.pdf","wb").write(requests.get("http://www.wsp.wa.gov/fire/docs/sprinkler/conall.pdf").content)
	call(["pdftotext", "-layout", "fir_c_WAwsp.pdf"])

	info = []
	for line in open("fir_c_WAwsp.txt", "r"):
	    if "License" not in line and "Currently" not in line and "Contact Name" not in line and "information" not in line and "of 29" not in line:
	        nline = re.sub("   *", "_%_", line)
	        nline = re.sub("\n", "", nline)
	        nline = nline.split("_%_")
		for item in nline:
			info.append(item)
		if "(" in line:
			l.info("\"" + "\"|\"".join(info) + "\"\n")
			f.write("\"" + "\"|\"".join(info) + "\"\n")
			info = []


if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception as e:
                l.critical(str(e))
	finally:
		f.close()
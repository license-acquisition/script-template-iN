import requests,re
from subprocess import call
import codecs
import time
from script_template import create_file, logger

f = create_file('roo_c_KSdoh', 'w', ['12', '37', '21', '13', 'first', 'last', '4', '36', '32', '6'])
l = logger('roo_c_KSdoh')

def main():
	open("roo_c_KSdoh.pdf", "wb").write(requests.get("http://ag.ks.gov/docs/default-source/documents/roofing-registration-applicants-by-business-name.pdf?sfvrsn=169").content) 
	call(["pdftotext", "-layout", "roo_c_KSdoh.pdf"])

	for line in open("roo_c_KSdoh.txt", "r"):
		nline = re.sub("   *", "_%_", line)
		nline = re.sub("\n", "", nline)
		nline = nline.split("_%_")
		if len(nline) > 4:
			nline.append("Roofer Registration")
			nline.append("1")
			l.info(nline)
			f.write("|".join(nline) + "\n")

if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception as e: l.critical(str(e))
	finally:
		f.close()
		call(['rm', 'roo_c_KSdoh.pdf'])
		call(['rm', 'roo_c_KSdoh.txt'])
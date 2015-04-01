import requests, re
from subprocess import call
from script_template import create_file, logger

f = create_file('fir_c_NVfmo', 'w', ['32', '7', '21', '37', '20'])
l = logger('fir_c_NVfmo')

def main():
	open("fir_c_NVfmo.pdf", "wb").write(requests.get("http://fire.nv.gov/uploadedFiles/firenvgov/content/bureaus/FPL/WebsiteList09152014.pdf").content)
	call(["pdftotext", "-layout", "fir_c_NVfmo.pdf"])

	for line in open("fir_c_NVfmo.txt", "r"):
		if "Business" in line:
			pass
		else:
			nline = re.sub("   *", "_%_", line)
			nline = re.sub("\n", "", nline)
			nline = nline.split("_%_")
			if len(nline) > 4:
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
import requests, re
from subprocess import call
from BeautifulSoup import BeautifulSoup
open("temp.pdf", "w").write(requests.get("http://fire.nv.gov/uploadedFiles/firenvgov/content/bureaus/FPL/WebsiteList09152014.pdf").content)
call(["pdftotext", "-layout", "temp.pdf"])

f = open("fir_c_NVfmo_20140915_000.csv", "w")
f.write("License Type, Business Name, License #, License Status, Renewal Date\n")
for line in open("temp.txt", "r"):
	if "Business" in line:
		pass
	else:
		nline = re.sub("   *", "_%_", line)
		nline = re.sub("\n", "", nline)
		nline = nline.split("_%_")
		if len(nline) > 4:
			f.write("\"" + "\",\"".join(nline) + "\"\n")



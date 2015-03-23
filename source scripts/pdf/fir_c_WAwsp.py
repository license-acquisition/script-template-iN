import requests, re
from subprocess import call
import requests
import time
stamp = time.strftime("%Y%m%d")
f = open("fir_WAdnr_%s_000.csv"%(stamp), "w")
f.write("entity_name,address\n")
s = requests.session()
open("conall.pdf","w").write(requests.get("http://www.wsp.wa.gov/fire/docs/sprinkler/conall.pdf").content)
call(["pdftotext", "-layout", "conall.pdf"])
data = []
for line in open("conall.txt", "r"):
    if "License" not in line and "Currently" not in line and "Contact Name" not in line and "information" not in line and "of 29" not in line:
        nline = re.sub("   *", "_%_", line)
        nline = re.sub("\n", "", nline)
        nline = nline.split("_%_")
	print nline
	for item in nline:
		data.append(item)
	if "(" in line:
		print("\"" + "\"|\"".join(data) + "\"\n")
		f.write("\"" + "\"|\"".join(data) + "\"\n")
		data = []


f.close()

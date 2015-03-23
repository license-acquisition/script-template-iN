import requests,re
from subprocess import call
import codecs
import time
open("roo_c_KSdoh.pdf", "w").write(requests.get("http://ag.ks.gov/docs/default-source/documents/roofing-registration-applicants-by-business-name.pdf?sfvrsn=169").content) 
call(["pdftotext", "-layout", "roo_c_KSdoh.pdf"])
f = open("roo_c_KSdoh_%s_000.csv"%(time.strftime("%Y%m%d")),"w")
f.write("entity_name,status,license_number,expiration_date,first,last,city,state,licensee_type_cd,company_flag\n")
for line in open("roo_c_KSdoh.txt", "r"):
        nline = re.sub("   *", "_%_", line)
        nline = re.sub("\n", "", nline)
        nline = nline.split("_%_")
        if len(nline) > 4:
		nline.append("Roofer Registration")
		nline.append("1")
		print "\"" + "\",\"".join(nline) + "\"\n"
                f.write("\"" + "\",\"".join(nline) + "\"\n")
f.close()

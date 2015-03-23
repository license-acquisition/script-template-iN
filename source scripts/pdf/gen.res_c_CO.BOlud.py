import requests, re
from subprocess import call
from BeautifulSoup import BeautifulSoup
feeds = ['con-ele-gen.com-gen.res_c_CO.BOlud_20140707_000', 'gen.res-roo_c_CO.BOlud_20140707_000', 'ele-gen.res-hva-plu_c_CO.BOlud_20140707_000','hva-plu_c_CO.BOlud_20140707_000','bui-car-gen.res-til_c_CO.BOlud_20140707_000','bui-gen.res-rem_c_CO.BOlud_20140707_000','bui-rem_c_CO.BOlud_20140707_000']
for a in BeautifulSoup(requests.get("http://www.bouldercounty.org/property/build/pages/buildinglicensedcontractors.aspx").content).findAll("a"):
	try:
		if ".pdf" in a['href']:
			open("well.pdf", "w").write(requests.get("http://www.bouldercounty.org%s"%a['href']).content)
			call(["pdftotext", "-layout", "well.pdf"])
			f = open("%s.csv"%feeds.pop(), "w")
			f.write("Company, Name, License Number, Address, Issue Date, City, State, Zip, Expiration Date, Phone, Permits Issued, Email\n")
			info = []
			for line in open("well.txt", "r"):
				if not any(s in line for s in ['Class A','Class B','Class C','Class M','Roof Con','Res Mech','Comm Mech','of 43','of 25','of 16','of 10','of 13','of 28','of 29','Land Use Dep','Licensed Contractors','Courthouse','P.O. Box 471','bouldercounty.org','303-441-3930']):
					nline = re.sub("   *", "_%_", line)
					nline = re.sub("\n", "", nline)
					nline = nline.split("_%_")
					if line.strip() == "" and len(info) > 4:
						if info[0] == "Finish" or info[0] == "Repair":
							del(info[0])
						if len(info) == 11:
							info[3] = info[3] + " " + info[5]
							info[5] = info[7]
							info[7] = info[9]
							info[9] = info[10]
							del(info[10])
						elif len(info) == 10 and "@" not in info[9]:
							info[3] = info[3] + " " + info[5]
							info[5] = info[7]
							info[7] = info[9]
							info[9] = " "
						info[5] = "\",\"".join(info[5].replace(",", "").rsplit(" ", 2))
						f.write("\"" + "\",\"".join(info).replace("Boulder County License:", "").replace("Issue Date:", "").replace("ExpirationDate:", "").replace("Permits Issued :", "") + "\"\n")
						info = []
					else:
						for item in nline:
							if item.strip() != "":
								info.append(item)
			f.close()
	except:
		pass







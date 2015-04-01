# *******************
# PDF scrape of IL licensed boiler repair firms
# Source: http://www.sfm.illinois.gov/commercial/boilers/licensedrepair.aspx

# Modified for reccurence by Anthony Nault
# 9/16/2014
# *******************

# Note: PDF to text does not work properly on my mac. The format should be good when this code is run on other machines though. - Anthony

# Note: Address parsing for this PDF is probalby best reserved for an Excel macro.

import requests, re, codecs, time
from subprocess import call
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('hva_c_ILsfm', 'w', ['12', '21', '0', '33', '6', '32', '102'])
l = logger('hva_c_ILsfm')

def main():
	open('hva_c_ILsfm.pdf', 'wb').write(requests.get('http://www.sfm.illinois.gov/Portals/0/docs/Commercial/Boilers/LicensedRepairFirmsListMay162014.pdf').content)
	call(["pdftotext", "-layout", "hva_c_ILsfm.pdf"])

	info = []
	for line in open("hva_c_ILsfm.txt", "r"):
		if ("BPV LICENSED REPAIR FIRMS" not in line and "Updated" not in line and "REPAIR FIRM NAME" not in line and "Page" not in line and "c/: rosa/documents/LicenseRepairFirms" not in line) and line.strip() != "":

			line = re.sub('\s\s+(?=\()|\s\s+(?=#)|(?<=\d)\s\s+(?=\d|[A-Z])', '|', line.replace('\n',''))
			line = line.split('|')
			for item in line:
				info.append(item)
			info.append("1") # company_flag
			info.append("Boiler Repair Firm") # licensee_type_cd
			info.append("License Number") # number_type

			f.write("|".join(info) + "\n")
			l.info(info)
			info = []


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()

















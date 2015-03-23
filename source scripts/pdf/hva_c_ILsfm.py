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

# =============== Download PDF from website ==============

# Name the file you want your PDF to become.
g = codecs.open('hva_c_ILsfm.pdf', 'wb')

# Go to source website and try to find the link to dowload the pdf.
print "Checking the web for PDF link..."
url = 'http://www.sfm.illinois.gov/commercial/boilers/licensedrepair.aspx'
page = requests.get(url)
soup = BeautifulSoup(page.content)
links = soup.find_all('a')

contractor_link = ""

try:
	# Try to find the right download link.
	for link in links:
		# Find the right download link on the page. Get the content of that PDF and write it to our PDF place holder.
		if "Boiler Licensed Repair Firms in Illinois" in link.text: # Insert link text of PDF download link.
			print "I found the link!"
			print "Downloading PDF..."
			contractor_link = link['href'][5:]

			# Get the last verfied date that is contained in the link text.
			verified_date = re.search('\d\d/\d\d/\d\d\d\d', link.text).group()
			verified_date = verified_date.split('/')
			month = str(verified_date[0])
			day = str(verified_date[1])
			year = str(verified_date[2])

			break # We don't want to check any more links!

	if contractor_link == "":
		# We did not find the link.
		sys.exit("FATAL ERROR! PDF not found. Check the source website for changes.")

except Exception as e:
	print str(e)
	sys.exit("PDF failed to download. Check the source website for changes.")

contractor_pdf = 'http://www.sfm.illinois.gov' + contractor_link

# Download PDF.
g.write(requests.get(contractor_pdf).content)
g.close()

print "PDF has been downloaded!"

# Convert PDF to TEXT (using pdftotext, duh)
call(["pdftotext", "-layout", "hva_c_ILsfm.pdf"])

print "PDF has been converted to text!"

# ================== Parse ===============================

f = codecs.open('hva_c_ILsfm_%s_000.txt' % (time.strftime('%Y%m%d')), 'w', 'UTF-8') 

# Define Headers for data.
headers = ["entity_name", "license_number", "address", "phone", "company_flag", "licensee_type_cd", "number_type"]
f.write("|".join(headers) + "\n")

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
		print "\"" + "\",\"".join(info) + "\"\n"
		info = []

f.close()

















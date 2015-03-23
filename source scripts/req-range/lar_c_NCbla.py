
import requests, time
import re
from bs4 import BeautifulSoup
import codecs

# North Carolina Lanscape Architects

# Business Name, Address, State, Zip , Phone, Fax, Email, License #, First Date, Thru Date

# From: http://www.ncbola.org/architect_directory.lasso?p=%x&-session=LASession:PeLUdqrXPI5kTja0YRmsjwLI4yzO7135864E21

f = codecs.open('lar_c_NCbla_%s_000.csv'%time.strftime('%Y%m%d'), 'w', 'utf-8')


headers = ["entity_name", "address1", "phone", "fax", "website", "license_number", "first_issue_date", "expiration_date"]
formline = ["", "", "", "", "", "", "", ""]
f.write("\"" + "\"|\"".join(headers) + "\"\n")

for x in range(1,10):
	url = "http://www.ncbola.org/firm_directory.lasso?p=%s-session=LASession:iN6yt9vSnd9LYORCHj1Vau6sgOxU3114A71423" %x
	page = requests.get(url)
	newcon = re.sub('<br>', ' ', page.content)
	newcon = re.sub('\n', ' ', newcon)
	soup = BeautifulSoup(newcon)

	mydivs = soup.findAll("div", {"class": "directoryitem"})

	for div in mydivs:
		fline = ''
		for x in div:
			if x.string:
				x.string = x.string.replace('\n',' ')
				fline =  fline +' _%_ '+ x.string.strip()
	
		formline[4] = ' '
		if 'Email:' in fline:
			#print fline
			newcon = re.sub('.*Email: _%_ ', '', fline)
			newcon = re.sub('_%_.*', '', newcon)
			formline[4] = newcon

		spl = fline.split('_%_')
		formline[0] = spl[2]

		spl = fline.split('Address:')
		spl = spl[1].split('_%_')
		formline[1] = spl[1]

		spl = fline.split('Phone:')
		spl = spl[1].split('_%_')
		formline[2] = spl[1]

		spl = fline.split('Fax:')
		spl = spl[1].split('_%_')
		formline[3] = spl[1]

		#spl = fline.split('Website:')
		#spl = spl[1].split('_%_')
		#formline[4] = spl[1]

		spl = fline.split('License Number:')
		spl = spl[1].split('_%_')
		formline[5] = spl[1]

		spl = fline.split('First Date of Licensure:')
		spl = spl[1].split('_%_')
		formline[6] = spl[1]

		spl = fline.split('Renewed Through Date:')
		spl = spl[1].split('_%_')
		formline[7] = spl[1]
		#sys.exit()
		fin = ''
		for n in formline:
			fin = fin + '\"' + n + '\"|'
		print fin + '\n'
		fin = re.sub('\n', '', fin)
		f.write(fin)
		f.write('\n')
		
		#sys.exit()
f.close()



import requests, time
import re
from bs4 import BeautifulSoup
import codecs
from script_template import create_file, logger

# North Carolina Lanscape Architects
# From: http://www.ncbola.org/architect_directory.lasso?p=%x&-session=LASession:PeLUdqrXPI5kTja0YRmsjwLI4yzO7135864E21

f = create_file('lar_c_NCbla', 'w', ['12', '0', '33', '66', '43', '21', '19', '13'])
l = logger('lar_c_NCbla')

def main():
        formline = ["", "", "", "", "", "", "", ""]
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
			l.info(fin)
			fin = re.sub('\n', '', fin)
			f.write(fin + '\n')
		

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()

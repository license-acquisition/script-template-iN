import requests, re, codecs, time
from subprocess import call
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('gen.res_c_ALesb', 'w', ['21', '7', '32', '0', '4', '36', '44', '35', '33'])
l = logger('gen.res_c_ALesb')

def main():
	soup = BeautifulSoup(requests.get("http://www.aesbl.alabama.gov/licensees.aspx").content)
	links = [a.attrs.get('href') for a in soup.select('#form1 > div.main > div.content_container > div > a')]
	url = "http://www.aesbl.alabama.gov/" + str(links[0])
	l.info(url)
	open("gen.res_c_ALesb.pdf", "wb").write(requests.get(url).content) 
	call(["pdftotext", "-layout", "-table", "gen.res_c_ALesb.pdf"])

	for line in open("gen.res_c_ALesb.txt", "r"):
		nline = re.sub("   *", "_%_", line)
		nline = re.sub("\n", "", nline)
		nline = nline.split("_%_")
		if len(nline) > 7:
			f.write("|".join(nline) + "\n")

if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception as e:
		l.critical(str(e))
	finally:
		f.close()
		call(['rm', 'gen.res_c_ALesb.pdf'])
		call(['rm', 'gen.res_c_ALesb.txt'])
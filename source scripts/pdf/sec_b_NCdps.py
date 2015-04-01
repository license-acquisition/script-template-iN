import requests, re, codecs, time
from bs4 import BeautifulSoup
from subprocess import call
from script_template import create_file, logger

f = create_file('sec_b_NCdps', 'w', ['21', '13', '35', '12', '0', 'city/state', '44', '33'])
l = logger('sec_b_NCdps')

def main():
	open('sec_b_NCdps.pdf', 'wb').write(requests.get('https://www.ncdps.gov/div/SBI/PPS/AlarmSystem/BurglarAlarmLicensees.pdf').content)
	call(["pdftotext", "-layout", "-table", "sec_b_NCdps.pdf"])

	info = []
	for line in open("sec_b_NCdps.txt","r"):
		if not any(s in line for s in ['Number', 'Private Protective', 'Burglar Alarm', 'Printed']):
			nline = re.sub("   *","_%_", line)
			nline = re.sub("\n", "", nline)
			nline = nline.split("_%_")
			for data in nline:
				if '(' in data:
					info.append(data.strip())
					info = [x for x in info if len(x) != 0]
					f.write('|'.join(info) + '\n')
					l.info(info)
					info = []
				else:
					info.append(data.strip())


if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception as e:
                l.critical(str(e))
	finally:
		f.close()
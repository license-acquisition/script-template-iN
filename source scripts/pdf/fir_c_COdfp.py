# fir_c_COdfp

import requests, re, codecs, time
from subprocess import call
from script_template import create_file, logger

f = create_file('fir_c_COdfp', 'w', ['7', '35', '0', 'city/state/zip', 'year', '21', '32'])
l = logger('fir_c_COdfp')

def main():
	call(['pdftotext', '-layout', '-table', 'fir_c_COdfp.pdf'])

	for line in open('fir_c_COdfp.txt', 'r'):
	    info = []
	    if len(line) > 1 and 'CityStateZip' not in line:
	        info = line.replace('\n','').split('  ')
	        info = [x.strip() for x in info if len(x) != 0]
	        f.write('|'.join(info) + '\n')
	       	l.info(info)


if __name__ == '__main__':
	try:
		main()
		l.info('complete')
	except Exception as e:
                l.critical(str(e))
	finally:
		f.close()

# shoutout to Anthony Nault for sound coding logic!
import re, codecs, time, requests
from subprocess import call
from urllib import urlretrieve
from script_template import create_file, logger

f = create_file('wel_c_WIdnr', 'w', ['21', '12', '33', 'phone2', 'address1/dba', '4', '36', '44', '11', '0'])
l = logger('wel_c_WIdnr')

def main():
    open('wel_c_WIdnr.pdf', 'wb').write(requests.get('http://dnr.wi.gov/topic/Wells/documents/WellDrillers.pdf').content)
    call(['pdftotext', '-layout', '-table', 'wel_c_WIdnr.pdf'])

    # split into a huge array
    rows = []
    for line in open('wel_c_WIdnr.txt', 'r'):
        if 'WELL DRILLERS' not in line and 'LIC#' not in line and 'Friday, January' not in line:
            if len(line) != 0:
                row = line.replace('\n','').split('  ')
                for part in row:
                    rows.append(part.strip())
    rows = [x for x in rows if len(x) != 0]

    # get index of comps
    index = []
    for i in range(len(rows)):
        try:
            if rows[i] == re.search(r'[0-9]{4}', rows[i]).group():
                index.append(i)
        except: pass

    # parse data string
    for i in range(len(index)-1):
        info = rows[index[i]:index[i+1]]
        if len([x for x, char in enumerate(info) if '(' in char]) != 2:
            info.insert(3, '')
        if len([x for x, char in enumerate(info) if '@' in char]) != 1:
            info.insert(5, '')
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
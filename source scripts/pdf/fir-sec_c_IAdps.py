# shoutout to Anthony Nault for sound coding logic!
import re, codecs, time, requests
from subprocess import call
from urllib import urlretrieve
from script_template import create_file, logger

f = create_file('fir-sec_c_IAdps', 'w', ['12', '21', '0', '4', '36', '44', '33', '13', '35', '32', '...', 'qualifying_individual2', 'licensee_type_cd2'])
l = logger('fir-sec_c_IAdps')

def main():
    open('fir-sec_c_IAdps.pdf', 'wb').write(requests.get("http://www.dps.state.ia.us/fm/building/alarm/PDFS/AlarmContractorsListing.pdf").content)
    call(["pdftotext", "-layout", "-table", "fir-sec_c_IAdps.pdf"])

    # split into a huge array
    rows = []
    for line in open('fir-sec_c_IAdps.txt', 'r'):
        if 'Iowa Department of' not in line and 'State Fire Marsh' not in line and 'Alarm System Lic' not in line and 'Des Moines, IA 50319' not in line and '(515) 725-6145' not in line and 'Business Name' not in line and 'Friday, February' not in line:
            if len(line) != 0:
                row = line.replace('\n','').split('  ')
                for part in row:
                    rows.append(part.strip())
    rows = [x for x in rows if len(x) != 0 and 'RME:' not in x]

    # get index of comps
    index = []
    for i in range(len(rows)):
        try:
            re.search(r'AC-[0-9]{3}', rows[i]).group()
            index.append(i-1)
        except: pass

    # parse data string
    for i in range(len(index)-1):
        f.write('|'.join(rows[index[i]:index[i+1]]) + '\n')


if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
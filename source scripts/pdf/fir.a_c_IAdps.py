import requests, re, time, codecs
from subprocess import call
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('fir.a_c_IAdps', 'w', ['7', '21', '0', '4', '36', '44', '13', '35', '78'])
l = logger('fir.a_c_IAdps')

def main():
    open("fir.a_c_IAdps.pdf", "wb").write(requests.get("http://www.dps.state.ia.us/fm/building/fesccp/PDFs/FESCCP_CertContractors.pdf").content)
    call(["pdftotext", "-layout", "-table", "fir.a_c_IAdps.pdf"])

    # split into a huge array
    rows = []
    for line in open('fir.a_c_IAdps.txt', 'r'):
        if not any(s in line for s in ['Iowa Department', 'State Fire Marsha', '215 E Seventh', 'Wednesday, Feb', 'Des Moines, IA 50319','515) 725-6145','Licensed Fire Protection']):
            if len(line) > 1:
                #row = re.sub("   *", "|", line)
                row = line.replace('\n','').split('  ')
                for part in row:
                    rows.append(part.strip())
    rows = [x.strip() for x in rows if len(x) != 0]
    rows = [x for x in rows if not any(s in x for s in ['Expiration:', 'RME:'])]

    # get index of comps
    index = []
    for i in range(len(rows)):
        try:
            if rows[i] == re.search(r'FP-[0-9]{3}', rows[i]).group():
                index.append(i)
        except: pass

    # parse data string
    for i in range(len(index)-1):
        info = rows[index[i]-1:index[i+1]-1]
        f.write('|'.join(info) + '\n')
        l.info(info)
    info = rows[index[len(index)-1]-1:]
    f.write('|'.join(info) + '\n')
   

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally:
        f.close()
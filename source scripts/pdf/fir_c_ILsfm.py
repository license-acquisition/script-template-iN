import requests, re, time, codecs
from subprocess import call
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('fir_c_ILsfm', 'w', ['7', '0', '4', '36', '44', '21', 'start_date', '13', '19', '32', '37'])
l = logger('fir_c_ILsfm')

def main():
        open("fir_c_ILsfm.pdf", "wb").write(requests.get("http://www.sfm.illinois.gov/Portals/0/FirePreventionDocs/LicensedFireSprinklerContractors.pdf").content)
        call(["pdftotext", "-layout", "-table", "fir_c_ILsfm.pdf"])

        lines = codecs.open('fir_c_ILsfm.txt', 'r').readlines()

        info = []
        for i in range(len(lines)):
                if len(lines[i]) > 1 and not any(s in lines[i] for s in ['License Detail','Search Criteria','JURISDICTION ONLINE','Praeses Corporation','License #']):
                        for data in lines[i].replace('\n', '').split('  '):
                                info.append(data.strip())
        info = [x for x in info if len(x) != 0]

        index1 = [x for x, char in enumerate(info) if char == 'License']
        for i in index1: # joining spacing between 'Fire Sprinkler Contractor' and 'License'
                info[i-1] = ' '.join([info[i-1], info[i]])
        info = [x for x in info if x != 'License']

        index = [x for x, char in enumerate(info) if 'Active' in char or 'Lapsed' in char]
                      
        for j in range(len(index)):
                if j == len(index)-1:
                        info2 = info[index[j]-6:]
                else:
                        info2 = info[index[j]-6:index[j+1]-6]
                if len(info2) == 8:
                        info2[0] = ' '.join([info2[0],info2[1]])
                        del(info2[1])
                addrs = info2[0]
                del(info2[0])
                info2.insert(0, addrs.rsplit(',', 2)[0].rsplit('-',1)[0].strip()) # company_name
                info2.insert(1, addrs.rsplit(',', 2)[0].rsplit('-',1)[1].strip()) # address1
                info2.insert(2, addrs.rsplit(',', 2)[1].strip()) # city
                info2.insert(3, addrs.rsplit(',',2)[2].strip()[:2]) # state
                info2.insert(4, addrs.rsplit(',',2)[2].strip()[2:].strip()) # zip
                l.info(info2)
                if len(info2) == 11:
                        f.write('|'.join(info2) + '\n')
                        info2 = []



if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
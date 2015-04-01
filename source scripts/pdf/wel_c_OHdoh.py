import requests, re, time, codecs
from subprocess import call
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('wel_c_OHdoh', 'w', ['21', '12', '35', 'YEAR', '0', '33', '4', '36', '44', '19', '37'])
l = logger('wel_c_OHdoh')

def main():
        open("wel_c_OHdoh.pdf", "wb").write(requests.get("http://www.odh.ohio.gov/~/media/ODH/ASSETS/Files/eh/water/Lists/List_RegPWSC_Ohio.ashx").content)
        call(["pdftotext", "-layout", "-table", "wel_c_OHdoh.pdf"])

        lines = codecs.open('wel_c_OHdoh.txt', 'r').readlines()

        info = []
        for i in range(len(lines)):
                if len(lines[i]) > 1 and not any(s in lines[i] for s in ['Ohio Department','Contractor Activity','Well  Spring','Total Number of','of 85']):
                        for data in lines[i].replace('\n', '').split('  '):
                                info.append(data.strip())
        info = [x.replace(')','').replace('(','') for x in info if len(x) != 0 and x!='X']

        index1 = [x for x, char in enumerate(info) if char=='Active']
        index2 = []
        for k in range(len(info)):
                try:
                        re.search(r'[0-9]{6}', info[k]).group()
                        index2.append(k)
                except:
                        pass
                
        for j in range(len(index1)):
                if j == len(index1)-1:
                        info2 = info[index1[j]-8:]
                else:
                        info2 = info[index2[j]:index1[j]+1]
                try:
                        addrs = info2[6]
                        del(info2[6])
                        info2.insert(6, addrs.rsplit(' ',2)[0].strip()) # city
                        info2.insert(7, addrs.rsplit(' ',2)[1].strip()) # state
                        info2.insert(8, addrs.rsplit(' ',2)[2].strip()) # zip
                except:
                        pass
                if len(info2) == 11:
                        l.info(info2)
                        f.write('|'.join(info2) + '\n')



if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
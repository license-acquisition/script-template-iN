import requests, re, time, codecs
from subprocess import call
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('fir_c_ILsfm', 'w', ['7', '0', '4', '36', '44', '21', 'start_date', '13', '19', '32', '37'])
l = logger('fir_c_ILsfm')

def main():
        open("fir_c_ILsfm.pdf", "wb").write(requests.get("http://www.sfm.illinois.gov/Portals/0/FirePreventionDocs/LicensedFireSprinklerContractors.pdf").content)
        call(["pdftotext", "-layout", "-table", "fir_c_ILsfm.pdf"])

        info = []
        for line in open('fir_c_ILsfm.txt', 'r'):
                if not any(s in line for s in ['License Detail', 'Search Criteria', 'JURISDICTION', 'Copyright', 'License #']):
                        if 'FSC' in line:
                                for data in line.split('  '):
                                        info.append(data.strip())
                                info = [x.strip() for x in info if len(x) != 0]
                                f.write('|'.join(info)+'\n')
                                l.info(info)
                                info = []
                        else:
                                row = line.split('-')
                                info.append(row[0].strip()) #company_name
                                try:
                                        addrs = row[1].rsplit(',', 2)
                                        info.append(addrs[0].strip()) #address1
                                        info.append(addrs[1].strip()) #city
                                        info.append(addrs[2].split(' ')[0]) #state
                                        info.append(addrs[2].split(' ')[1]) #zip
                                except:
                                        pass



if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
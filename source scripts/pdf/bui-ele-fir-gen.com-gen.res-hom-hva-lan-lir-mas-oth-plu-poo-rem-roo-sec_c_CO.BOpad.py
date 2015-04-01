import requests, re, time, codecs
from subprocess import call
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('bui-ele-fir-gen.com-gen.res-hom-hva-lan-lir-mas-oth-plu-poo-rem-roo-sec_c_CO.BOpad', 'w', ['7', '21', '32', '32', '13', 'address1/city/state/zip', 'phone_number_type', '33', '35', '22'])
l = logger('bui-ele-fir-gen.com-gen.res-hom-hva-lan-lir-mas-oth-plu-poo-rem-roo-sec_c_CO.BOpad')

def main():
        for a in BeautifulSoup(requests.get("https://bouldercolorado.gov/plan-develop/hiring-a-contractor").content).find_all("a"):
                
                try:
                        if ".pdf" in a['href']:
                                open("well.pdf", "wb").write(requests.get(a['href']).content)
                                call(["pdftotext", "-layout", "-table", "well.pdf"])
                                info = []
                                l.debug('found pdf. Now acquiring...')
                                license_types = []
                                start = False
                                count = 0
                                for line in open("well.txt","r"):
                                        if len(line) > 1 and not any(s in line for s in ['CITY OF BOULDER', '1739 Broadway,', '303-441-1880', 'as of ', 'Company Name', 'Printed on']):
                                                nline = re.sub("   *", "_%_", line)
                                                nline = re.sub("\n","",nline)
                                                nline = nline.split("_%_")
                                               
                                                try:
                                                        
                                                        if (not start) and (len(nline) > 5):
                                                                for i in range(0, len(nline)):
                                                                        info.append(nline[i])
                                                                start = True
                                                                count += 1
                                                                                  
                                                        elif (start) and (count == 1) and (len(nline) > 0):
                                                                info.append(nline[0])
                                                                if len(nline) > 1:
                                                                        for i in range(1, len(nline)):
                                                                                license_types.append(nline[i])
                                                                count += 1
                                                        elif start and len(nline) > 1:
                                                                info.append(nline[1])
                                                                if len(nline) > 2:
                                                                        for i in range(2, len(nline)):
                                                                                license_types.append(nline[i])
                                                                if nline[0] == "Responsible:":
                                                                        start = False
                                                                        count = 0
                                                                        info.extend(license_types)
                                                                        
                                                                        f.write('|'.join(info) + '\n')
                                                                        info = []
                                                                        license_types = []
                                                except Exception, e:
                                                        l.error(str(e))
                                                 
                except Exception, e:
                        l.error(str(e))
                        continue

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.close()
import requests, re, codecs, time
from subprocess import call
from bs4 import BeautifulSoup

#open("well.pdf", "w").write(requests.get("http://www.mass.gov/lwd/docs/dos/lead-asbestos/asbestos/web-list-ac.pdf").content)
#call(["pdftotext", "-layout", "-table", "well.pdf"])

f = codecs.open('asb_c_MAdls_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['license_number', 'expiration_date', 'company_name', 'company_name2', 'address1', 'address2', 'city/state/zip', 'phone', 'clean_helpers']
f.write('|'.join(headers) + '\n')

g = codecs.open('asb_c_MAdls.txt', 'r')
lines = g.readlines()
g.close()

dewey = []
malcolm = []
reese = []
for line in lines:
        if 'This  List' not in line and 'Currently Licensed Asbestos' not in line and 'This List' not in line and 'The licensing information' not in line and 'expiration date of the li' not in line and 'contractor beginning' not in line and 'contract beginning any' not in line and 'Generated On:' not in line:
                columns = line.replace('\n','').split('\t')
                if len(columns) == 4:
                        dewey.append(''.join([columns[0],columns[1]]).strip())
                        malcolm.append(columns[2].strip())
                        reese.append(columns[3].strip())

count = 0
for column in [dewey, malcolm, reese]:
        row = 1
        info = []
        for line in column:
                if len(line) == 0:
                        pass
                elif 'Expires:' in line:
                        info = []
                        info.append(line)
                elif len([i for i, char in enumerate(line) if char == '-']) == 2:
                        info.append(line)
                        info = [x.replace('"','') for x in info if len(x) != 0]
                        info.insert(1, info[0].split('Expires:')[0].strip())
                        info.insert(2, info[0].split('Expires:')[1].strip())
                        del(info[0])
                        print len(info)
                        if len(info) == 7:
                                try: # company is two rows
                                        int(info[4][0])
                                        info.insert(5,'')
                                except: # address is two rows
                                        info.insert(3, '')
                        elif len(info) == 6:
                                info.insert(3, '')
                                info.insert(5, '')
                        info.append(str(row))
                        f.write('|'.join(info) + '\n')
                        print info
                        row += 1
                        count += 1
                        info = []
                else:
                        info.append(line)
print count
f.write('The numbers at the end of the rows appear 3x. The pdf was a 3 column pdf, so weird numbers \n')
f.write('that appear in the license_number column correspond to missing expiration_dates. Might not be worth it to fix. \n')
f.close()
                        
                        
                        

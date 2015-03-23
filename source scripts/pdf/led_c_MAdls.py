import requests, re, codecs, time
from subprocess import call
from bs4 import BeautifulSoup

#open("well.pdf", "w").write(requests.get("http://www.mass.gov/lwd/docs/dos/lead-asbestos/lead/la-rpt-list-dc.pdf").content)
#call(["pdftotext", "-layout", "-table", "led_c_MAdls.pdf"])

f = codecs.open('led_c_MAdls_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['license_number', 'expiration_date', 'qualifying_individual', 'company_name', 'address1', 'address2', 'city/state/zip', 'phone', 'HasEmployees', 'clean_helpers']
f.write('|'.join(headers) + '\n')

g = codecs.open('led_c_MAdls.txt', 'r')
lines = g.readlines()
g.close()

dewey = []
malcolm = []
reese = []
for line in lines:
        if 'Renovation Work' not in line and 'Currently' not in line and 'Ordered by Town' not in line and 'The licensing information' not in line and 'expiration date of the li' not in line and 'contractor beginning' not in line and 'Generated On:' not in line:
                columns = line.replace('\n','').split('\t')
                if len(columns) == 8:
                        dewey.append(''.join([columns[0],columns[1],columns[2]]).strip())
                        malcolm.append(''.join([columns[3],columns[4],columns[5],columns[6]]).strip())
                        reese.append(columns[7].strip())

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
                elif 'Has Employees:' in line:
                        info.append(line)
                        info = [x.replace('"','') for x in info if len(x) != 0]
                        info.insert(1, info[0].split('Expires:')[0].strip()) #license_number
                        info.insert(2, info[0].split('Expires:')[1].strip()) #expiration_date
                        del(info[0])
                        last = info.pop()
                        info.append(last.split('Has Employees:')[0].strip()) #phone
                        info.append(last.split('Has Employees:')[1].strip()) #employees
                        print len(info)
                        '''
                        if len(info) == 8:
                                try: # company is two rows
                                        int(info[3][0])
                                        info.insert(3,'')
                                except: # address is two rows
                                        info.insert(3, '')
                        elif len(info) == 7:
                                info.insert(3, '')
                                info.insert(5, '')
                        '''
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

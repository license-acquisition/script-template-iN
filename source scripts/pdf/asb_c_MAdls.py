import requests, re, codecs, time
from subprocess import call
from bs4 import BeautifulSoup
from script_template import create_file, logger

f = create_file('asb_c_MAdls', 'w', ['21', '13', '7', 'company_name2', '0', '1', 'city/state/zip', '33', 'clean_helpers'])
l = logger('asb_c_MAdls')

def main():
        #open("asb_c_MAdls.pdf", "wb").write(requests.get("http://www.mass.gov/lwd/docs/dos/lead-asbestos/asbestos/web-list-ac.pdf").content)
        #call(["pdftotext", "-layout", "-table", "asb_c_MAdls.pdf"])

        dewey = []
        malcolm = []
        reese = []
        lines = []
        for line in open('asb_c_MAdls.txt', 'r'):
                if 'This  List' not in line and 'Currently Licensed Asbestos' not in line and 'This List' not in line and 'The licensing information' not in line and 'expiration date of the li' not in line and 'contractor beginning' not in line and 'contract beginning any' not in line and 'Generated On:' not in line:
                        columns = line.replace('\n', '').split('\t')
                        dewey.append(columns[0].strip())
                        malcolm.append(columns[1].strip())
                        reese.append(columns[2].strip())

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
                                l.info(info)
                                row += 1
                                count += 1
                                info = []
                        else:
                                info.append(line)


if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e:
                l.critical(str(e))
        finally:
                f.write('The numbers at the end of the rows appear 3x. The pdf was a 3 column pdf, so weird numbers \n')
                f.write('that appear in the license_number column correspond to missing expiration_dates. Might not be worth it to fix. \n')
                f.close()

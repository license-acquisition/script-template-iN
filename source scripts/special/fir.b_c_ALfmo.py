'''
Christopher jimenez

http://www.firemarshal.alabama.gov/Reports/PrintAllSprinklers.aspx
'''
import time, requests, codecs
from bs4 import BeautifulSoup
from script_template import create_file, logger

f1 = create_file('fir.b_c_ALfmo', 'w', ['12', '0', '33', '21', '37', '19', '13', '35'])
l1 = logger('fir.b_c_ALfmo')
f2 = create_file('fir.a_c_ALfmo', 'w', ['7', '0', '33', '21', '37', 'CertificationHolder', 'HolderStatus', 'LicensedAs', '19', '13'])
l2 = logger('fir.a_c_ALfmo')

def main():
        try:
                #sprinkler()
                l1.info('complete')
        except Exception as e:
                l1.critical(str(e))
        finally:
                f1.close()
        try:
                alarm()
                l2.info('complete')
        except Exception as e:
                l2.critical(str(e))
        finally:
                f2.close()

def sprinkler():
	soup = BeautifulSoup(requests.get('http://www.firemarshal.alabama.gov/Reports/PrintAllSprinklers.aspx').content)
	tds = soup.find_all('td')
	for i in range(0, len(tds), 8):
		info = []
		info.append(tds[0 + i].text)
		info.append(tds[1 + i].text)
		info.append(tds[2 + i].text)
		info.append(tds[3 + i].text)
		info.append(tds[4 + i].text)
		info.append(tds[5 + i].text)
		info.append(tds[6 + i].text)
		info.append(tds[7 + i].text)
		f1.write('|'.join(info) + '\n')
		l1.info(info)

def alarm():
        soup = BeautifulSoup(open('alarm.html', 'r'))
        trs = soup.find_all('tr', {'align': 'center'})
        l2.debug(len(trs))
        for tr in trs:
                tds = tr.find_all('td')
                info = []
                for td in tds:
                        info.append(td.text)
                del(info[0])
                f2.write("|".join(info) + "\n")
                l2.info(info)
        '''
        tds = soup.find_all('td')
        l2.debug(len(tds))
        for i in range(0, len(tds), 11):
                try:
                        info = []
                        info.append(tds[1 + i].text)
                        info.append(tds[2 + i].text)
                        info.append(tds[3 + i].text)
                        info.append(tds[4 + i].text)
                        info.append(tds[5 + i].text)
                        info.append(tds[6 + i].text)
                        info.append(tds[7 + i].text)
                        info.append(tds[8 + i].text)
                        info.append(tds[9 + i].text)
                        info.append(tds[10 + i].text)
                        f2.write("|".join(info) + "\n")
                        l2.info(info)
                except Exception as e:
                        l2.error(str(e))
        '''                

if __name__ == "__main__":
        try:
                main()
        except Exception as e:
                pass

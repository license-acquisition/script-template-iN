import codecs, re, requests, csv, time
from bs4 import BeautifulSoup
from datetime import date
from script_template import create_file, logger

f = create_file('arc-eng_c_NEbea', 'w', ['12', '21', '32', '35', 'qualifying_individual2', '78', '37', '4', '8', '36', 'country', '19', '13', '6', '102'])
l = logger('arc-eng_c_NEbea')

def main():
        for i in range(0, 5000):
                try:
                        url = "http://www.ea.nebraska.gov/search/search.php?page=details&lic=CA%04d" %i
                        soup = BeautifulSoup(requests.get(url).content)

                        info = []
                        info.append(soup.find_all("p", {"class" : "center"})[0].find("span", {"class" : "bold"}).text)
                        for span in soup.find_all("span", {"class" : "bold"}):
                                span.decompose()
                        for p in soup.find_all("p", {"class" : "label"}):
                                info.append(p.text)

                        #fix 1st parsing issue             
                        if len(info)==12:
                                info.insert(4," ")
                        info.append("1")
                        info.append("license number")

                        f.write('|'.join(info) + '\n')
                        l.info(info)
                
                except Exception as e:
                        l.error(str(e))

if __name__ == '__main__':
        try:
                main()
                l.info('complete')
        except Exception as e: l.critical(str(e))
        finally: f.close()
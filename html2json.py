#################################
# Scraping to non-normalized json
# Ex: Oklahoma
#################################
import requests, codecs, json
from bs4 import BeautifulSoup

url = 'http://www.deq.state.ok.us/aqdnew/lbp/Certified%20Lists/CertifiedLBPFirms.html'
soup = BeautifulSoup(requests.get(url).content)

source = {}
count = 0
for tr in soup.find_all('tr'):
    info = []
    for td in tr.find_all('td'):
        info.append(td.text.strip())
    source[count] = info
    count += 1

f = codecs.open('html2json.txt', 'w')
json.dump(source, f)
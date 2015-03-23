from bs4 import BeautifulSoup
import codecs, re, csv, requests, time

start = time.time()
f = codecs.open('led_i_MDdoe_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')
headers = ['expiration_date', 'company_name', 'phone', 'city', 'state', 'zip', 'license_number',
           'address1', 'fax', 'qualifying_individual', 'licensee_type_cd', 'RegionsOfOper', 'Types of Work Performed']
f.write('|'.join(headers) + '\n')

# get soup
url = 'http://www.mde.state.md.us/programs/Land/LeadPoisoningPrevention/HomeOwners/Pages/Programs/LandPrograms/LeadCoordination/homeowners/search/LeadContractors.aspx?all=1'
soup = BeautifulSoup(requests.get(url).content)
# get all links on page
links = []
for link in soup.find_all('a'):
    try:
        if 'LeadContractorDetails' in link['href']:
            links.append(link['href'])
    except: pass
    
# get line info for help with parsing later
expiry, company, addrs, phone = [], [], [], []
tds = soup.find_all('table', {'cellpadding': '5'})[0].find_all('td', {'class': 'ms-vb'})
print len(tds)
for i in range(0, len(tds), 4):
    expiry.append(tds[i].text.strip())
    company.append(tds[i+1].text.strip())
    addrs.append(tds[i+2].text.strip())
    phone.append(tds[i+3].text.strip())
    
# iterate through links and scrape
shortie = 'http://www.mde.state.md.us/programs/Land/LeadPoisoningPrevention/HomeOwners/Pages/Programs/LandPrograms/LeadCoordination/homeowners/search/'
num_iter = 0 # for matching with addrs list
for link in links:
    info = []
    soup = BeautifulSoup(requests.get(shortie + link).content)
    tds = soup.find_all('td', {'class': 'ms-vb'})
    print len(tds)
    # append stuff I already have
    info.append(expiry[num_iter]) # expiration_date
    info.append(company[num_iter]) # company_name
    info.append(phone[num_iter]) # phone
    info.append(addrs[num_iter].split(',')[0].strip()) # city
    info.append(addrs[num_iter].split(',')[1].strip()[:2]) # state
    info.append(addrs[num_iter].split(',')[1].strip()[2:]) # zip
    # parse stuff
    info.append(tds[0].text.split(':')[1].strip()) # license_number
    info.append(tds[6].text.split(addrs[num_iter])[0].strip()) # address1
    info.append(tds[10].text.strip()) # fax
    info.append(tds[12].text.strip()) # qualifying_individual

    # append long parts
    data = [x.text.replace('\n','').replace('\r','') for x in tds[13:]]
    index1 = data.index('ACCREDITATION')
    index2 = data.index('REGIONS OF OPERATION')
    index3 = data.index('TYPES OF WORK PERFORMED')
    info.append(', '.join([x.strip() for x in data[index1+1:index2]])) # licensee_type_cd
    info.append(', '.join([x.strip() for x in data[index2+1:index3]])) # regions of op
    info.append(', '.join([x.strip() for x in data[index3+1:]])) # types of work
        
    print info
    f.write('|'.join(info) + '\n')
    num_iter += 1

f.write('Minutes elapsed: %s' %((time.time()-start)/60))
f.close()

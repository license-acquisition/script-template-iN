from bs4 import BeautifulSoup
import codecs, re, csv, requests, time
from script_template import create_file, logger

f = create_file('led_c_MDdoe', 'w', ['13', '7', '33', '4', '36', '44', '21', '0', '66', '35', '32', 'RegionsOfOper', 'Types of Work Performed'])
l = logger('led_c_MDdoe')

def main():
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
            
        l.info(info)
        f.write('|'.join(info) + '\n')
        num_iter += 1

if __name__ == '__main__':
    try:
        main()
        l.info('complete')
    except Exception as e:
        l.critical(str(e))
    finally: f.close()
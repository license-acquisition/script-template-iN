###################################
# Output: output.txt
# Method: selenium + requests
###################################

# Import modules #########################################

import codecs, requests
from bs4 import BeautifulSoup
from selenium import webdriver

from script_template import create_file, logger
       

# Write file and headers #################################

f = create_file('type_entityType_authority', 'w', ['canonical header indexes'])
#headers = ['canonical_header1', 'canonical_header2', 'canonical_header3', '...']


# Set up logging ########################################
l = logger('authority')

# Create file for links
u = codecs.open('authority_links.csv', 'w', 'utf-8')

###########################################
# Many sites require selenium to click through pages
# that result from searching license types from a dropdown
# menu. While clicking through pages, we collect the links.
# Afterwards, we request each link and parse the data
############################################

# Initialize driver and request session #########################

driver = webdriver.Chrome()
s = requests.Session()

# We often need to open an instance of the page to create
# cookies for later requests
s.get('initial splash page.com')


# Open page and click stuff on form input #######################
def get_page(n):
    driver.get('initial splash page.com')
    license_types = [1,2,3,4] # make sure to make a comment on what the numbers refer to
    driver.find_element_by_xpath('xpath to drop down element %s' %license_types[n]).click()
    driver.find_element_by_xpath('xpath to search button').click()

# Grab links from each results page ##############################
def grab_links():
    for link in BeautifulSoup(driver.page_source).find_all('a'):
        if 'details/lice_no' in link['href']:
            u.write(link['href'] + '\n')


# Scrape links from links file ####################################
def scrape_links(n):
    i = 1
    check = True
    while check:
        try:
            grab_links()
            i+=1
            driver.find_element_by_link_text('%s' %i).click()
        except:
            if len(driver.find_elements_by_link_text('...')) == 1:
                n += 1
                if n >= 4: # ie it has scraped the last page
                    break
                else:
                    get_page(n) # get next license_type
                    i = 1

            elif len(driver.find_elements_by_link_text('...')) == 0:
                n += 1
                if n >= 4: # ie it has scraped the last page
                    break
                else:
                    get_page(n) # get next license_type
                    i = 1
            elif len(driver.find_elements_by_link_text('...')) == 1:
                driver.find_element_by_link_text('...').click()
            elif len(driver.find_elements_by_link_text('...')) == 2:
                driver.find_elements_by_link_text('...')[1].click()

# Parsing function -> always different from site to site #####
def authority_name(link):
    try:
        soup = BeautifulSoup(s.get('link from link.csv'.replace('\n','')).content)
        info = []
        '''

        PARSE however you want 
        info.append(soup.find('tag', {'id': 'unique'}).text.strip())

        '''   
        l.info(info) # use logs instead of print since EC2 does not have multiple consoles
        f.write('|'.join(info) + '\n')

# iterate through link file and get data
def get_data():
    for line in open('link.csv', 'r'):
        KSbtp(line)

# Main logic ##############################################
if __name__ == '__main__':     
    try:
        n = 0
        get_page(n)
        scrape_links(n)
        get_data()
        l.('COMPLETE')
    except Exception as e:
        l.critical(str(e))

    finally:               
        f.close()
        driver.quit()
    

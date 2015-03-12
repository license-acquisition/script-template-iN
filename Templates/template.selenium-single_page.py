###################################
# Output: output.txt
# Method: selenium, single-page
###################################

# Import modules #########################################

import codecs, re, requests, time
from bs4 import BeautifulSoup
from selenium import webdriver

       
# Write file and headers #################################

f = codecs.open('type_entityType_authority_%s_000.txt' %(time.strftime('%Y%m%d')), 'w', 'utf-8')

headers = ['canonical_header1', 'canonical_header2', 'canonical_header3', '...']

f.write('|'.join(headers) + '\n') # all write code should include a new-line ('\n') character at end

# Set up logging ########################################

def log(status):

    feed = 'type_entityType_authority_%s_000.txt' %(time.strftime('%Y%m%d'))  # date in output
    
    l = codecs.open('log.csv', 'a')
    
    l.write(','.join([feed, str(time.strftime('%Y/%m/%d')), str(time.time()), status]) + '\n')


###########################################
# Script is composed of opening webpage in selenium and
# clicking a few buttons to output a single page of
# results. Then parse the results table.
############################################

# Initialize driver #####################################

driver = webdriver.PhantomJS()


# Navigate to page, click form options and search ########

def main():

    driver.get('www.authority_site.whatevs')

    driver.find_elements_by_tag_name('tag')[0].click()

    driver.find_elements_by_tag_name('search')[0].click()


    # Soupify the page and parse

    info = []

    soup = BeautifulSoup(driver.page_source)

    '''

    Parse - - - -

    '''

    print info

    f.write('|'.join(info) + '\n')


# Main logic ############################################

if __name__ == '__main__':
    
    log('START')

    try:

        main()

        log('COMPLETE')

    except: log('ERROR')

    finally:
                     
        f.close()

        driver.quit()

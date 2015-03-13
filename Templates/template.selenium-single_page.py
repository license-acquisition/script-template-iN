###################################
# Output: output.txt
# Method: selenium, single-page
###################################

# Import modules #########################################

import codecs, re, requests, time
from bs4 import BeautifulSoup
from selenium import webdriver
from script_template import create_file, logger
       
# Write file and headers #################################

f = create_file('type_entityType_authority', 'w', [headers array])

###########################################
# Script is composed of opening webpage in selenium and
# clicking a few buttons to output a single page of
# results. Then parse the results table.
############################################

# Initialize driver #####################################

driver = webdriver.PhantomJS()


# Navigate to page, click form options and search ########

def main():

    try:

        logger(f.name, 'START')

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

        logger(f.name, 'COMPLETE')

    except:

        logger(f.name, 'ERROR', 'explanation') # explanation is an optional thing

    finally:

        f.close()

        driver.quit()


# Main logic ############################################

if __name__ == '__main__':
    
    main()

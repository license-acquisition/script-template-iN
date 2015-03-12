#####################
# Output: output.txt
# Method: requests, form data
#####################

# Import modules #########################################

import codecs, re, requests, time
from bs4 import BeautifulSoup

       
# Write file and headers #################################

f = codecs.open('type_entityType_authority_%s_000.txt' %(time.stftime('%Y%m%d')), 'w', 'utf-8')

headers = ['canonical_header1', 'canonical_header2', 'canonical_header3', '...']

f.write('|'.join(headers) + '\n') # all write code should include a new-line ('\n') character at end

def log(status):
    # Set up logging ########################################

    feed = 'feed_name_%s_000.txt' %(time.strftime('%Y%m%d'))  # date in output

    l = codecs.open('log.csv', 'a')
    # feed|date|timestampe|status
    l.write(','.join([feed, str(time.strftime('%Y/%m/%d')), str(time.time()), status]) + '\n')


#########################################################
# Some sites allow post requests which can be written into
# the url via form data.
# Example: www.site.com?key1=value1&key2=value2
##########################################################

def main():
    # Hit the initial page ###################################
    # It's usually the navigation, form-input page ###########

    url = 'initial url to hit'

    soup = BeautifulSoup(requests.get(url).content)

    # Get all elements which will be used in iteration url ###
    # loop through form data inputs ##########################
    for element in soup.find_all('element'):
        
        iteration_url = 'url with added form data'
        
        soup = BeautifulSoup(requests.get(iteration_url).content)
        
        for link in soup.find_all("a"):
            
            try:
                
                # look for commonalities in link urls
                if 'details/lic_number=' in link['href']:
                    
                    # get the soup where the actual data is!!
                    detailed_soup = BeautifulSoup(requests.get(link['href']).content)
                    
                    info = [] # list for appending license data

                    '''

                    parse the page source in any way you need to, then write to file

                    '''

                    print info

                    f.write('|'.join(info) + '\n')
                    
            except Exception, e:
                
                    print str(e)


# Main logic #################################################

if __name__ == '__main__':

    log('START')

    try:

        main()

        log('COMPLETE')

    except: log('ERROR')

    finally: f.close()
